class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def get_average_homework(self):
        if not self.grades:
            return 0
        else:
            all_grades = []
            for grade in self.grades.values():
                all_grades.extend(grade)
            return sum(all_grades)/len(all_grades)
    
    def __str__(self):
        courses = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (
            f'Имя: {self.name} \nФамилия: {self.surname}\n'+
            f'Средняя оценка за домашние задания: {self.get_average_homework()}\n'+
            f'Курсы в процессе изучения: {courses}\n'+
            f'Завершенные курсы: {finished_courses}'
        )
    def rate_lecture(self, lecturer, course, grade):
        if  isinstance(lecturer,Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
                return f"Оценка {grade} за курс {course} поставлена лектору {lecturer.name} { lecturer.surname}"
            else:
                lecturer.grades[course] = [grade]
                return f"Оценка {grade} за курс {course} поставлена лектору {lecturer.name} { lecturer.surname}"
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
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'
    
    
class Lecturer(Mentor):
    def __init__(self,name,surname):
        super().__init__(name,surname) 
        self.grades = {}
        
        
    def get_average_lecturer(self):
        if not self.grades:
            return 0
        all_grades = []
        for grade in self.grades.values():
            all_grades.extend(grade)
        return sum(all_grades)/len(all_grades)
    
    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname} \n'
                f'Средняя оценка за лекции: {self.get_average_lecturer()}')
    

class Reviewer(Mentor):
    def __init__(self,name,surname):
        super().__init__(name,surname)
        
    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}'
    
    # def rate_hw(self,student,course,grade)



lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')

# Настраиваем курсы
student.courses_in_progress += ['Python', 'Java', 'C++']  # Добавили C++ для студента
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']
reviewer.rate_hw(student, 'Python', 10)
reviewer.rate_hw(student, 'Python', 9)
reviewer.rate_hw(student, 'C++', 8)
student.finished_courses += ['Введение в программирование']
# Ставим оценки
print(student.rate_lecture(lecturer, 'Python', 7))   # Успех
print(student.rate_lecture(lecturer, 'Python', 9))   # Успех
print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка (лектор не ведёт Java)
print(student.rate_lecture(lecturer, 'C++', 8))      # Успех (теперь C++ есть у студента)
print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка (reviewer не Lecturer)

# Выводим результаты
print("\n" + str(reviewer))
print("\n" + str(lecturer))
print(f"\nСредняя оценка лектора: {lecturer.get_average_lecturer()}")
print(f"Словарь оценок лектора: {lecturer.grades}")
print(f"Атрибуты лектора: {lecturer.__dict__}")

 
 
print(lecturer.__dict__) 
print(student.__str__())
print(student.grades)