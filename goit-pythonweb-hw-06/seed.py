import random
from datetime import date, timedelta

from faker import Faker
from sqlalchemy import delete

from src.db import session_scope
from src.models import Grade, Group, Student, Subject, Teacher

NUMBER_OF_GROUPS = 3
NUMBER_OF_TEACHERS = 4
NUMBER_OF_SUBJECTS = 6
NUMBER_OF_STUDENTS = 40
MAX_GRADES_PER_STUDENT_PER_SUBJECT = 5

GROUP_NAMES = ["AD-101", "AD-102", "AD-103"]

SUBJECT_POOL = [
    "Mathematics",
    "Physics",
    "Computer Science",
    "Databases",
    "Algorithms",
    "Operating Systems",
    "Networks",
    "Linear Algebra",
]

fake = Faker()


def random_date():
    return date.today() - timedelta(days=random.randint(0, 120))


def seed():
    with session_scope() as session:
        session.execute(delete(Grade))
        session.execute(delete(Subject))
        session.execute(delete(Student))
        session.execute(delete(Teacher))
        session.execute(delete(Group))

        groups = [Group(name=name) for name in GROUP_NAMES[:NUMBER_OF_GROUPS]]
        session.add_all(groups)
        session.flush()

        teachers = [Teacher(full_name=fake.name()) for _ in range(NUMBER_OF_TEACHERS)]
        session.add_all(teachers)
        session.flush()

        subject_names = random.sample(SUBJECT_POOL, k=NUMBER_OF_SUBJECTS)
        subjects = [
            Subject(name=name, teacher_id=random.choice(teachers).id)
            for name in subject_names
        ]
        session.add_all(subjects)
        session.flush()

        students = [
            Student(full_name=fake.name(), group_id=random.choice(groups).id)
            for _ in range(NUMBER_OF_STUDENTS)
        ]
        session.add_all(students)
        session.flush()

        grades = []
        for student in students:
            for subject in subjects:
                count = random.randint(0, MAX_GRADES_PER_STUDENT_PER_SUBJECT)
                for _ in range(count):
                    grades.append(
                        Grade(
                            student_id=student.id,
                            subject_id=subject.id,
                            grade=round(random.uniform(60, 100), 2),
                            date_received=random_date(),
                        )
                    )
        session.add_all(grades)

        print(
            f"Seeded: {len(groups)} groups, {len(teachers)} teachers, "
            f"{len(subjects)} subjects, {len(students)} students, "
            f"{len(grades)} grades."
        )


if __name__ == "__main__":
    seed()
