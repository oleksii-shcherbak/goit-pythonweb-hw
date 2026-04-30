from sqlalchemy import desc, func, select

from src.db import session_scope
from src.models import Grade, Group, Student, Subject


def select_1():
    with session_scope() as session:
        stmt = (
            select(Student.full_name, func.round(func.avg(Grade.grade), 2).label("avg"))
            .join(Grade, Grade.student_id == Student.id)
            .group_by(Student.id)
            .order_by(desc("avg"))
            .limit(5)
        )
        return [(name, float(avg)) for name, avg in session.execute(stmt).all()]


def select_2(subject_id):
    with session_scope() as session:
        stmt = (
            select(Student.full_name, func.round(func.avg(Grade.grade), 2).label("avg"))
            .join(Grade, Grade.student_id == Student.id)
            .where(Grade.subject_id == subject_id)
            .group_by(Student.id)
            .order_by(desc("avg"))
            .limit(1)
        )
        row = session.execute(stmt).first()
        return (row[0], float(row[1])) if row else None


def select_3(subject_id):
    with session_scope() as session:
        stmt = (
            select(Group.name, func.round(func.avg(Grade.grade), 2).label("avg"))
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .where(Grade.subject_id == subject_id)
            .group_by(Group.id)
            .order_by(Group.name)
        )
        return [(name, float(avg)) for name, avg in session.execute(stmt).all()]


def select_4():
    with session_scope() as session:
        stmt = select(func.round(func.avg(Grade.grade), 2))
        result = session.execute(stmt).scalar()
        return float(result) if result is not None else None


def select_5(teacher_id):
    with session_scope() as session:
        stmt = (
            select(Subject.name)
            .where(Subject.teacher_id == teacher_id)
            .order_by(Subject.name)
        )
        return [name for (name,) in session.execute(stmt).all()]


def select_6(group_id):
    with session_scope() as session:
        stmt = (
            select(Student.full_name)
            .where(Student.group_id == group_id)
            .order_by(Student.full_name)
        )
        return [name for (name,) in session.execute(stmt).all()]


def select_7(group_id, subject_id):
    with session_scope() as session:
        stmt = (
            select(Student.full_name, Grade.grade)
            .join(Grade, Grade.student_id == Student.id)
            .where(Student.group_id == group_id, Grade.subject_id == subject_id)
            .order_by(Student.full_name, Grade.date_received)
        )
        return [(name, float(grade)) for name, grade in session.execute(stmt).all()]


def select_8(teacher_id):
    with session_scope() as session:
        stmt = (
            select(func.round(func.avg(Grade.grade), 2))
            .join(Subject, Subject.id == Grade.subject_id)
            .where(Subject.teacher_id == teacher_id)
        )
        result = session.execute(stmt).scalar()
        return float(result) if result is not None else None


def select_9(student_id):
    with session_scope() as session:
        stmt = (
            select(Subject.name)
            .join(Grade, Grade.subject_id == Subject.id)
            .where(Grade.student_id == student_id)
            .group_by(Subject.id)
            .order_by(Subject.name)
        )
        return [name for (name,) in session.execute(stmt).all()]


def select_10(student_id, teacher_id):
    with session_scope() as session:
        stmt = (
            select(Subject.name)
            .join(Grade, Grade.subject_id == Subject.id)
            .where(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
            .group_by(Subject.id)
            .order_by(Subject.name)
        )
        return [name for (name,) in session.execute(stmt).all()]


def select_11(student_id, teacher_id):
    with session_scope() as session:
        stmt = (
            select(func.round(func.avg(Grade.grade), 2))
            .join(Subject, Subject.id == Grade.subject_id)
            .where(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        )
        result = session.execute(stmt).scalar()
        return float(result) if result is not None else None


def select_12(group_id, subject_id):
    with session_scope() as session:
        latest_date = session.execute(
            select(func.max(Grade.date_received))
            .join(Student, Student.id == Grade.student_id)
            .where(Student.group_id == group_id, Grade.subject_id == subject_id)
        ).scalar()
        if latest_date is None:
            return []

        stmt = (
            select(Student.full_name, Grade.grade)
            .join(Grade, Grade.student_id == Student.id)
            .where(
                Student.group_id == group_id,
                Grade.subject_id == subject_id,
                Grade.date_received == latest_date,
            )
            .order_by(Student.full_name)
        )
        return [(name, float(grade)) for name, grade in session.execute(stmt).all()]
