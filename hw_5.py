class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def add_score(self, lecturer, course, score_number):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress and int(score_number) in range(1,11):
            if course in lecturer.grades:
                lecturer.grades[course] += [score_number]
            else:
                lecturer.grades[course] = [score_number]
        else:
            return "Произошла ошибка."

    def everage_rating (self):
        list_of_grades = list(map(sum, self.grades.values()))
        return round(sum(list_of_grades) / len(list_of_grades), 2)

    def __str__(self):
        some_student = f'Имя: {self.name} \n' \
                       f'Фамилия: {self.surname} \n' \
                       f'Средняя оценка за домашнее задание: {self.everage_rating()} \n' \
                       f'Курсы в процессе изучения: {self.courses_in_progress} \n' \
                       f'Завершенные курсы: {self.finished_courses}'
        return some_student

    def __lt__(self, other):
        if not isinstance(other, Student):
            return "Это не студент"
        return self.everage_rating() < other.everage_rating()

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def everage_rating (self):
        list_of_scores = list(map(sum, self.grades.values()))
        return round(sum(list_of_scores) / len(list_of_scores), 2)

    def __str__(self):
        some_lecturer = f'Имя: {self.name} \n' \
                        f'Фамилия: {self.surname} \n' \
                        f'Средняя оценка за лекции: {self.everage_rating()}'
        return some_lecturer

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return "Это не лектор"
        return self.everage_rating() < other.everage_rating()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        some_reviewer = f'Имя: {self.name} \n' \
                        f'Фамилия: {self.surname}'
        return some_reviewer


#функция одна и для студентор, и для лекторов
def average_course_grade(people, course):
    list_of_scores = []
    for person in people:
        m = sum(person.grades[course])
        list_of_scores.append(m)
    return round((sum(list_of_scores)) / len(list_of_scores), 2)



# best_student = Student('Ruoy', 'Eman', 'your_gender')
# best_student.courses_in_progress += ['Python']
#
# cool_mentor = Mentor('Some', 'Buddy')
# cool_mentor.courses_attached += ['Python']
#
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)

#print(best_student.grades)

# students, their courses
st1 = Student('Ruoy', 'Eman', 'male')
st1.courses_in_progress += ['ruby']
st1.courses_in_progress += ["python"]
st1.add_courses("philosophy")

st2 = Student('John', 'Smith', 'male')
st2.courses_in_progress += ["math"]
st2.courses_in_progress += ["python"]
st2.add_courses("philosophy")

list_of_students = [st1, st2]

# reviewers, students' grades
reviewer1 = Reviewer('Leo', 'Orlov')
reviewer1.courses_attached += ['ruby']
reviewer1.courses_attached += ['python']
reviewer1.rate_hw(st1, 'ruby', 6)
reviewer1.rate_hw(st1, 'python', 7)
reviewer1.rate_hw(st1, 'python', 5)
reviewer1.rate_hw(st2, 'python', 3)
reviewer1.rate_hw(st2, 'python', 8)

reviewer2 = Reviewer('Gleb', 'Ivanov')
reviewer2.courses_attached += ['math']
reviewer2.rate_hw(st2, 'math', 8)
#print(st2.grades)

#lecturers, lecturers' scores
lecturer1 = Lecturer('Mary', 'Stone')
lecturer1.courses_attached += ["ruby"]
lecturer1.courses_attached += ["python"]

st1.add_score(lecturer1, "ruby", 6)
st1.add_score(lecturer1, "python", 5)
st1.add_score(lecturer1, "python", 8)
st2.add_score(lecturer1, "python", 2)
st2.add_score(lecturer1, "python", 9)

lecturer2 = Lecturer('Kate', 'Crowach')
lecturer2.courses_attached += ["math"]
lecturer2.courses_attached += ["python"]
st2.add_score(lecturer2, "math", 10)
st1.add_score(lecturer2, "python", 8)

list_of_lecturers = [lecturer1, lecturer2]

print(st1)
print()
print(st2)
print()
print(lecturer1)
print()
print(lecturer2)
print()
print("Средняя оценка студента 1: ", st1.everage_rating())
print()
print("Средняя оценка студента 2: ", st2.everage_rating())
print()
print("Средняя оценка лектора 1: ", lecturer1.everage_rating())
print()
print("Средняя оценка лектора 2: ", lecturer2.everage_rating())
print()
print(lecturer1.__lt__(lecturer2))
print()
print(st1.__lt__(st2))
print(average_course_grade(list_of_students, 'python'))
print(average_course_grade(list_of_lecturers, 'python'))

