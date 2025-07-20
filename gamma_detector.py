import numpy as np
from matplotlib import pyplot as plt

E_Na = np.array([0.01, 0.05, 0.1, 0.5, 1.0])
sigma_ph_Na = np.array([1e3, 1e2, 50, 1, 0.1]) * 1e-24
sigma_comp_Na = np.array([5, 10, 8, 5, 3]) * 1e-24

E_I = np.array([0.01, 0.05, 0.1, 0.5, 1.0])
sigma_ph_I = np.array([1e4, 5e3, 1e3, 10, 1]) * 1e-24
sigma_comp_I = np.array([10, 15, 12, 8, 5]) * 1e-24


def interpolate_sigma(E, E_table, sigma_table):
    idx = np.searchsorted(E_table, E, side='right') - 1
    if idx < 0:
        return sigma_table[0]
    elif idx >= len(E_table) - 1:
        return sigma_table[-1]
    else:
        return sigma_table[idx] + (E - E_table[idx]) * (sigma_table[idx + 1] - sigma_table[idx]) / (
                    E_table[idx + 1] - E_table[idx])


def macro_cross_sections(E_gamma):
    density = 3.67
    molar_mass_NaI = 149.89
    Na = 6.022e23
    N_NaI = density * Na / molar_mass_NaI * 2

    sigma_ph_Na_val = interpolate_sigma(E_gamma, E_Na, sigma_ph_Na)
    sigma_comp_Na_val = interpolate_sigma(E_gamma, E_Na, sigma_comp_Na)
    sigma_ph_I_val = interpolate_sigma(E_gamma, E_I, sigma_ph_I)
    sigma_comp_I_val = interpolate_sigma(E_gamma, E_I, sigma_comp_I)

    sigma_ph = (sigma_ph_Na_val + sigma_ph_I_val) / 2
    sigma_comp = (sigma_comp_Na_val + sigma_comp_I_val) / 2

    mu_photo = sigma_ph * N_NaI
    mu_comp = sigma_comp * N_NaI

    return mu_comp, mu_photo


def compton_scatter(E_gamma):
    mc2 = 511.0
    cos_theta = 1 - 2 * np.random.random()
    E_scattered = E_gamma / (1 + (E_gamma / mc2) * (1 - cos_theta))
    E_e = E_gamma - E_scattered
    return E_scattered, E_e, cos_theta


def simulate_spectrum(R, D, source_pos, E_gamma, num_events):
    spectrum = np.zeros(1024)
    E_max = 1500.0

    for _ in range(num_events):
        theta = np.arccos(2 * np.random.random() - 1)
        phi = 2 * np.pi * np.random.random()
        direction = np.array([
            np.sin(theta) * np.cos(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(theta)
        ])

        t_entry = ray_cylinder_intersection(R, D, source_pos, direction)
        if t_entry is None:
            continue

        pos = np.array(source_pos) + t_entry * direction
        deposited_energy = 0.0
        current_E = E_gamma
        current_dir = direction.copy()

        while True:
            mu_comp, mu_photo = macro_cross_sections(current_E / 1000)
            mu_total = mu_comp + mu_photo

            if mu_total <= 0:
                break

            l = -np.log(np.random.random()) / mu_total
            new_pos = pos + l * current_dir

            if not (0 <= new_pos[2] <= D) or (new_pos[0] ** 2 + new_pos[1] ** 2 > R ** 2):
                if deposited_energy > 0:
                    channel = int((deposited_energy / E_max) * 1024)
                    if 0 <= channel < 1024:
                        spectrum[channel] += 1
                break

            if np.random.random() < mu_photo / mu_total:
                deposited_energy += current_E
                channel = int((deposited_energy / E_max) * 1024)
                if 0 <= channel < 1024:
                    spectrum[channel] += 1
                break
            else:
                E_scattered, E_e, cos_theta = compton_scatter(current_E)
                deposited_energy += E_e
                current_E = E_scattered

                phi = 2 * np.pi * np.random.random()
                theta = np.arccos(cos_theta)

                z_axis = current_dir / np.linalg.norm(current_dir)
                if np.abs(z_axis[2]) > 0.999:
                    x_axis = np.array([1.0, 0.0, 0.0])
                else:
                    x_axis = np.array([z_axis[1], -z_axis[0], 0.0])
                    x_axis /= np.linalg.norm(x_axis)
                y_axis = np.cross(z_axis, x_axis)

                local_dir = np.array([
                    np.sin(theta) * np.cos(phi),
                    np.sin(theta) * np.sin(phi),
                    np.cos(theta)
                ])

                new_dir = (
                        local_dir[0] * x_axis +
                        local_dir[1] * y_axis +
                        local_dir[2] * z_axis
                )
                new_dir /= np.linalg.norm(new_dir)

                current_dir = new_dir
                pos = new_pos

    return spectrum
def ray_cylinder_intersection(R, D, source_pos, direction):
    X0, Y0, Z0 = source_pos
    vx, vy, vz = direction
    a = vx ** 2 + vy ** 2
    b = 2 * (X0 * vx + Y0 * vy)
    c = X0 ** 2 + Y0 ** 2 - R ** 2
    D_eq = b ** 2 - 4 * a * c
    t_side = None
    if D_eq >= 0:
        t1 = (-b + np.sqrt(D_eq)) / (2 * a)
        t2 = (-b - np.sqrt(D_eq)) / (2 * a)
        for t in [t1, t2]:
            if t >= 0:
                z = Z0 + t * vz
                if 0 <= z <= D:
                    if t_side is None or t < t_side:
                        t_side = t
    t_caps = []
    if vz != 0:
        t_bottom = -Z0 / vz
        t_top = (D - Z0) / vz
        for t in [t_bottom, t_top]:
            if t >= 0:
                x = X0 + t * vx
                y = Y0 + t * vy
                if x ** 2 + y ** 2 <= R ** 2:
                    t_caps.append(t)
    t_min = None
    if t_side is not None:
        t_min = t_side
    if t_caps:
        t_cap_min = min(t_caps)
        if t_min is None or t_cap_min < t_min:
            t_min = t_cap_min
    return t_min


def simulate_spectrum(R, D, source_pos, E_gamma, num_events):
    spectrum = np.zeros(1024)
    E_max = 1500
    mu_comp, mu_photo = macro_cross_sections(E_gamma)
    mu_total = mu_comp + mu_photo

    for _ in range(num_events):
        theta = np.arccos(2 * np.random.random() - 1)
        phi = 2 * np.pi * np.random.random()
        direction = np.array([
            np.sin(theta) * np.cos(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(theta)
        ])

        t_entry = ray_cylinder_intersection(R, D, source_pos, direction)
        if t_entry is None:
            continue

        pos = np.array(source_pos) + t_entry * direction
        deposited_energy = 0
        current_E = E_gamma
        current_dir = direction.copy()

        while True:
            xi = np.random.random()
            l = -np.log(xi) / mu_total if mu_total > 0 else float('inf')
            new_pos = pos + l * current_dir

            if not (0 <= new_pos[2] <= D) or (new_pos[0] ** 2 + new_pos[1] ** 2 > R ** 2):
                if deposited_energy > 0:
                    channel = int(deposited_energy / E_max * 1024)
                    if 0 <= channel < 1024:
                        spectrum[channel] += 1
                break

            xi = np.random.random()
            if xi < mu_photo / mu_total:
                deposited_energy += current_E
                if np.random.random() < 0.8 and current_E > 33.2:
                    if np.random.random() < 0.8:
                        spectrum[int(28.5 / E_max * 1024)] += 0.8
                    else:
                        spectrum[int(32.5 / E_max * 1024)] += 0.2
                channel = int(deposited_energy / E_max * 1024)
                if 0 <= channel < 1024:
                    spectrum[channel] += 1
                break
            else:
                E_scattered, E_e, cos_theta = compton_scatter(current_E)
                deposited_energy += E_e
                current_E = E_scattered
                phi = 2 * np.pi * np.random.random()
                theta = np.arccos(cos_theta)

                z_axis = current_dir / np.linalg.norm(current_dir)
                if np.abs(z_axis[2]) > 0.999:
                    x_axis = np.array([1.0, 0.0, 0.0])
                else:
                    x_axis = np.array([z_axis[1], -z_axis[0], 0.0])
                    x_axis /= np.linalg.norm(x_axis)
                y_axis = np.cross(z_axis, x_axis)


                local_dir = np.array([
                    np.sin(theta) * np.cos(phi),
                    np.sin(theta) * np.sin(phi),
                    np.cos(theta)
                ])


                new_dir = (
                    local_dir[0] * x_axis +
                    local_dir[1] * y_axis +
                    local_dir[2] * z_axis
                )
                new_dir /= np.linalg.norm(new_dir)

                current_dir = new_dir
                pos = new_pos

    return spectrum



R, D = 5.0, 15.0
source_pos = (0.0, 0.0, -1.0)
E_gamma = 662
num_events = 100000

spectrum = simulate_spectrum(R, D, source_pos, E_gamma, num_events)
spectrum = np.convolve(spectrum, np.ones(5) / 5, mode='same')

plt.figure(figsize=(12, 6))
plt.plot(np.linspace(0, 1500, 1024), spectrum)
plt.xlabel('Энергия (кэВ)')
plt.ylabel('Количество событий')
plt.title('Симуляция спектра гамма-излучения в детекторе NaI')
plt.grid(True)
plt.show()