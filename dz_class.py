class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
    
    def __gt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_homework() > other.get_average_homework()
    
    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_homework() < other.get_average_homework()
    
    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_homework() == other.get_average_homework()
    
    def get_average_homework(self):
        if not self.grades:
            return 0
        all_grades = []
        for grade in self.grades.values():
            all_grades.extend(grade)
        return round(sum(all_grades) / len(all_grades), 1)
    
    def __str__(self):
        courses = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {self.get_average_homework()}\n'
                f'Курсы в процессе изучения: {courses}\n'
                f'Завершенные курсы: {finished_courses}')
    
    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
            return f"Оценка {grade} за курс {course} поставлена лектору {lecturer.name} {lecturer.surname}"
        else:
            return 'Ошибка'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
    
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
    
    def __gt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_lecturer() > other.get_average_lecturer()
    
    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_lecturer() < other.get_average_lecturer()
    
    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_lecturer() == other.get_average_lecturer()
    
    def get_average_lecturer(self):
        if not self.grades:
            return 0
        all_grades = []
        for grade in self.grades.values():
            all_grades.extend(grade)
        return round(sum(all_grades) / len(all_grades), 1)
    
    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.get_average_lecturer()}')


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
    
    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'
    
    def rate_hw(self, student, course, grade):
        result = super().rate_hw(student, course, grade)
        if result != 'Ошибка':
            return f'Ревьюер {self.name} оценил студента {student.name} по курсу {course}. Оценка: {grade}'
        return 'Ошибка'


# ============ ФУНКЦИИ ДЛЯ ПОДСЧЕТА СРЕДНИХ ОЦЕНОК ============

def average_student_grade(students_list, course_name):
    """Подсчет средней оценки студентов по курсу"""
    if not students_list:
        return 0
    all_grades = []
    for student in students_list:
        if isinstance(student, Student) and course_name in student.grades:
            all_grades.extend(student.grades[course_name])
    if not all_grades:
        return 0
    return round(sum(all_grades) / len(all_grades), 1)


def average_lecturer_grade(lecturers_list, course_name):
    """Подсчет средней оценки лекторов по курсу"""
    if not lecturers_list:
        return 0
    all_grades = []
    for lecturer in lecturers_list:
        if isinstance(lecturer, Lecturer) and course_name in lecturer.grades:
            all_grades.extend(lecturer.grades[course_name])
    if not all_grades:
        return 0
    return round(sum(all_grades) / len(all_grades), 1)


# ============ ПОЛЕВЫЕ ИСПЫТАНИЯ ============

# Создаем по 2 экземпляра каждого класса
student1 = Student("Иван", "Петров", "male")
student2 = Student("Мария", "Иванова", "female")

lecturer1 = Lecturer("Анна", "Смирнова")
lecturer2 = Lecturer("Петр", "Сидоров")

reviewer1 = Reviewer("Ольга", "Кузнецова")
reviewer2 = Reviewer("Дмитрий", "Волков")

# Настройка курсов
student1.courses_in_progress = ["Python", "Git", "Java"]
student2.courses_in_progress = ["Python", "Git"]

student1.finished_courses = ["Введение в программирование"]
student2.finished_courses = ["Введение в программирование", "Основы баз данных"]

reviewer1.courses_attached = ["Python", "Git"]
reviewer2.courses_attached = ["Python", "Java"]

lecturer1.courses_attached = ["Python", "Git"]
lecturer2.courses_attached = ["Python", "Java"]

# Выставление оценок студентам (через Reviewer)
reviewer1.rate_hw(student1, "Python", 5)
reviewer1.rate_hw(student1, "Python", 4)
reviewer1.rate_hw(student1, "Git", 5)
reviewer2.rate_hw(student2, "Python", 5)
reviewer2.rate_hw(student2, "Python", 5)
reviewer2.rate_hw(student2, "Java", 4)

# Выставление оценок лекторам (через Student)
student1.rate_lecture(lecturer1, "Python", 5)
student1.rate_lecture(lecturer1, "Python", 4)
student2.rate_lecture(lecturer2, "Python", 5)
student2.rate_lecture(lecturer2, "Java", 4)

# Проверка __str__
print("=== ИНФОРМАЦИЯ О СТУДЕНТАХ ===")
print(student1)
print()
print(student2)
print()

print("=== ИНФОРМАЦИЯ О ЛЕКТОРАХ ===")
print(lecturer1)
print()
print(lecturer2)
print()

print("=== ИНФОРМАЦИЯ О REVIEWER ===")
print(reviewer1)
print()
print(reviewer2)
print()

# Проверка сравнения студентов
print("=== СРАВНЕНИЕ СТУДЕНТОВ ===")
print(f"{student1.name} > {student2.name}: {student1 > student2}")
print(f"{student1.name} < {student2.name}: {student1 < student2}")
print(f"{student1.name} == {student2.name}: {student1 == student2}")
print()

# Проверка сравнения лекторов
print("=== СРАВНЕНИЕ ЛЕКТОРОВ ===")
print(f"{lecturer1.name} > {lecturer2.name}: {lecturer1 > lecturer2}")
print(f"{lecturer1.name} < {lecturer2.name}: {lecturer1 < lecturer2}")
print(f"{lecturer1.name} == {lecturer2.name}: {lecturer1 == lecturer2}")
print()

# Проверка функций подсчета средних оценок
print("=== СРЕДНИЕ ОЦЕНКИ ПО КУРСАМ ===")
students_list = [student1, student2]
lecturers_list = [lecturer1, lecturer2]

print(f"Средняя оценка студентов по курсу Python: {average_student_grade(students_list, 'Python')}")
print(f"Средняя оценка студентов по курсу Git: {average_student_grade(students_list, 'Git')}")
print(f"Средняя оценка студентов по курсу Java: {average_student_grade(students_list, 'Java')}")
print()
print(f"Средняя оценка лекторов по курсу Python: {average_lecturer_grade(lecturers_list, 'Python')}")
print(f"Средняя оценка лекторов по курсу Java: {average_lecturer_grade(lecturers_list, 'Java')}")
print(f"Средняя оценка лекторов по курсу Git: {average_lecturer_grade(lecturers_list, 'Git')}")