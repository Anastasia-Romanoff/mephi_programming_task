import _sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = _sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, create_table_query):
        """Создает таблицу."""
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_data(self, insert_query):
        """Вставляет данные в таблицу."""
        self.cursor.execute(insert_query)
        self.conn.commit()

    def select_data(self, select_query):
        """Выполняет запрос SELECT."""
        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.conn.close()


class DatabaseApplication:
    def __init__(self):
        self.students_db = DatabaseManager('sqlite_python.db')
        self.courses_db = DatabaseManager('sqlite_python_courses.db')
        self.student_courses_db = DatabaseManager('sqlite_python_Student_courses.db')


        self.create_students_table = '''CREATE TABLE Students (
                                        id INTEGER PRIMARY KEY,
                                        name text NOT NULL,
                                        surname text NOT NULL,
                                        age INTEGER,
                                        city text NOT NULL);'''

        self.insert_students_data = '''INSERT INTO Students VALUES (1, 'Max', 'Brooks', 24, 'Spb'),
                                        (2, 'John', 'Stones', 15, 'Spb'),
                                        (3, 'Andy', 'Wings', 45, 'Manhester'),
                                        (4, 'Kate', 'Brooks', 34, 'Spb')'''

        self.select_all_students = "SELECT * FROM Students"
        self.select_students_age_over_30 = "SELECT * FROM Students WHERE age > 30"

        self.create_courses_table = '''CREATE TABLE Courses (
                                        id INTEGER PRIMARY KEY,
                                        name text NOT NULL,
                                        time_start TEXT,
                                        time_end TEXT);'''

        self.insert_courses_data = '''INSERT INTO Courses VALUES (1, 'python', '2021-07-21', '2021-08-21'),
                                        (2, 'java', '2021-07-13', '2021-08-16')'''

        self.select_all_courses = "SELECT * FROM Courses"

        self.create_student_courses_table = '''CREATE TABLE Student_courses (
                                            course_id INTEGER,
                                            student_id INTEGER,
                                            FOREIGN KEY (student_id) REFERENCES  Students (id),
                                            FOREIGN KEY (course_id) REFERENCES  Courses (id));'''
        self.insert_student_courses_data = '''INSERT INTO Student_courses VALUES (1, 1),(2, 1),(3, 1),(4, 2)'''
        self.select_all_student_courses = "SELECT * FROM Student_courses"
        self.select_students_python_course = """
                  SELECT DISTINCT
                      s.*
                  FROM Students AS s
                  JOIN Student_courses AS sc ON s.id = sc.student_id
                  JOIN Courses AS c ON sc.course_id = c.id
                  WHERE c.name = 'python'
              """
        self.select_students_spb_python = """
                    SELECT DISTINCT
                        s.*
                    FROM Students AS s
                    JOIN Student_courses AS sc ON s.id = sc.student_id
                    JOIN Courses AS c ON sc.course_id = c.id
                    WHERE c.name = 'python'
                    AND s.city = 'Spb'
                """

    def create_and_populate_databases(self):
        self.students_db.create_table(self.create_students_table)
        self.students_db.insert_data(self.insert_students_data)
        print(self.students_db.select_data(self.select_all_students))
        print(f"Студенты старше 30 лет: {self.students_db.select_data(self.select_students_age_over_30)}")


        self.courses_db.create_table(self.create_courses_table)
        self.courses_db.insert_data(self.insert_courses_data)
        print(self.courses_db.select_data(self.select_all_courses))

        self.student_courses_db.create_table(self.create_student_courses_table)
        self.student_courses_db.insert_data(self.insert_student_courses_data)
        print(self.student_courses_db.select_data(self.select_all_student_courses))
        print(f"Студенты старше 30 лет: {self.students_db.select_data(self.select_students_age_over_30)}")
        

    def close_connections(self):
        self.students_db.close()
        self.courses_db.close()
        self.student_courses_db.close()


if __name__ == "__main__":
    app = DatabaseApplication()
    app.create_and_populate_databases()
    app.close_connections()