import math
def calculate_velocity():
        diss = float(input("Введите расстояние в км: "))
        time = float(input("Введите время в часах: "))
        velocity = diss/time
        print(f"Скорость: {velocity:.2f} км/ч")

def calculate_mass():
        force = float(input("Введите силу в Н: "))
        acceleration = float(input("Введите ускорениех в м/с2: "))
        mass  = force/acceleration
        print(f"Скорость: {mass:.2f} км/ч")

def calculate_celsius():
    fahrenheit = float(input("Введите температуру в градусах Фаренгейта: "))
    celsius = (fahrenheit - 32) * 5 / 9
    print(f"Температура в градусах Цельсия: {celsius:.2f} °C")

def calculate_work():
    force = float(input("Введите силу в ньютонах: "))
    distance = float(input("Введите расстояние в метрах: "))
    work = force * distance
    print(f"Работа: {work:.2f} Дж")

def calculate_kinetic_energy():
    mass = float(input("Введите массу объекта в килограммах: "))
    velocity = float(input("Введите скорость объекта в метрах в секунду: "))
    kinetic_energy = 0.5 * mass * velocity ** 2
    print(f"Кинетическая энергия: {kinetic_energy:.2f} Дж")

def calculate_potential_energy():
    mass = float(input("Введите массу в килограммах: "))
    height = float(input("Введите высоту в метрах: "))
    g = 9.81  
    potential_energy = mass * g * height
    print(f"Потенциальная энергия: {potential_energy:.2f} Дж")

def calculate_pressure():
    force = float(input("Введите силу в ньютонах: "))
    area = float(input("Введите площадь в квадратных метрах: "))
    pressure = force / area
    print(f"Давление: {pressure:.2f} Па")


def calculate_heat():
    mass = float(input("Введите массу в килограммах: "))
    specific_heat = float(input("Введите удельную теплоёмкость (Дж/(кг·°C)): "))
    temperature_change = float(input("Введите изменение температуры в градусах Цельсия: "))
    heat = mass * specific_heat * temperature_change
    print(f"Количество теплоты: {heat:.2f} Дж")

def calculate_frequency():
    period = float(input("Введите период колебаний в секундах: "))
    frequency = 1 / period 
    print(f"Частота: {frequency:} Гц")


def calculate_volume():
    radius = float(input("Введите радиус основания цилиндра в метрах: "))
    height = float(input("Введите высоту цилиндра в метрах: "))
    volume = math.pi * radius ** 2 * height 
    print(f"Объем цилиндра: {volume:} кубических метров")

def main():
    while True:
        print("Выбор задачи:")
        choice = input("Введите номер задачи 1-10: ")

        if choice == '1':
            calculate_velocity()
        elif choice == '2':
            calculate_mass()
        elif choice == '3':
            calculate_celsius()
        elif choice == '4':
            calculate_work()
        elif choice == '5':
            calculate_kinetic_energy()
        elif choice == '6':
            calculate_potential_energy()
        elif choice == '7':
            calculate_pressure()
        elif choice == '8':
            calculate_heat()
        elif choice == '9':
            calculate_frequency()
        elif choice == '10':
            calculate_volume()

        elif choice == 'q':
            break
    

if __name__ == "__main__":
    main()