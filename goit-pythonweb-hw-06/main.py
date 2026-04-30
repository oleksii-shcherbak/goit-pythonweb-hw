import argparse
import sys
from datetime import datetime

from src.db import session_scope
from src.models import Grade, Group, Student, Subject, Teacher

MODEL_MAP = {
    "Group": Group,
    "Teacher": Teacher,
    "Student": Student,
    "Subject": Subject,
    "Grade": Grade,
}


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def build_kwargs(model_name, args):
    if model_name in {"Group", "Teacher", "Student"}:
        kwargs = {}
        if args.name is not None:
            field = "name" if model_name == "Group" else "full_name"
            kwargs[field] = args.name
        if model_name == "Student" and args.group_id is not None:
            kwargs["group_id"] = args.group_id
        return kwargs

    if model_name == "Subject":
        kwargs = {}
        if args.name is not None:
            kwargs["name"] = args.name
        if args.teacher_id is not None:
            kwargs["teacher_id"] = args.teacher_id
        return kwargs

    if model_name == "Grade":
        kwargs = {}
        if args.student_id is not None:
            kwargs["student_id"] = args.student_id
        if args.subject_id is not None:
            kwargs["subject_id"] = args.subject_id
        if args.grade is not None:
            kwargs["grade"] = args.grade
        if args.date is not None:
            kwargs["date_received"] = parse_date(args.date)
        return kwargs

    raise ValueError(f"Unsupported model: {model_name}")


def format_row(obj):
    if isinstance(obj, Group):
        return f"Group(id={obj.id}, name={obj.name!r})"
    if isinstance(obj, Teacher):
        return f"Teacher(id={obj.id}, full_name={obj.full_name!r})"
    if isinstance(obj, Student):
        return (
            f"Student(id={obj.id}, full_name={obj.full_name!r}, "
            f"group_id={obj.group_id})"
        )
    if isinstance(obj, Subject):
        return (
            f"Subject(id={obj.id}, name={obj.name!r}, teacher_id={obj.teacher_id})"
        )
    if isinstance(obj, Grade):
        return (
            f"Grade(id={obj.id}, student_id={obj.student_id}, "
            f"subject_id={obj.subject_id}, grade={obj.grade}, "
            f"date_received={obj.date_received.isoformat()})"
        )
    return repr(obj)


def cmd_create(model_name, args):
    model_cls = MODEL_MAP[model_name]
    kwargs = build_kwargs(model_name, args)
    with session_scope() as session:
        instance = model_cls(**kwargs)
        session.add(instance)
        session.flush()
        print(f"Created: {format_row(instance)}")


def cmd_list(model_name, _args):
    model_cls = MODEL_MAP[model_name]
    with session_scope() as session:
        rows = session.query(model_cls).order_by(model_cls.id).all()
        if not rows:
            print(f"No {model_name} records found.")
            return
        for row in rows:
            print(format_row(row))


def cmd_update(model_name, args):
    if args.id is None:
        sys.exit("--id is required for update")

    model_cls = MODEL_MAP[model_name]
    kwargs = build_kwargs(model_name, args)
    if not kwargs:
        sys.exit("No fields provided to update.")

    with session_scope() as session:
        instance = session.get(model_cls, args.id)
        if instance is None:
            sys.exit(f"{model_name} with id={args.id} not found.")
        for field, value in kwargs.items():
            setattr(instance, field, value)
        session.flush()
        print(f"Updated: {format_row(instance)}")


def cmd_remove(model_name, args):
    if args.id is None:
        sys.exit("--id is required for remove")

    model_cls = MODEL_MAP[model_name]
    with session_scope() as session:
        instance = session.get(model_cls, args.id)
        if instance is None:
            sys.exit(f"{model_name} with id={args.id} not found.")
        session.delete(instance)
        print(f"Removed: {model_name} id={args.id}")


ACTIONS = {
    "create": cmd_create,
    "list": cmd_list,
    "update": cmd_update,
    "remove": cmd_remove,
}


def build_parser():
    parser = argparse.ArgumentParser(description="CRUD CLI for the university database.")
    parser.add_argument("-a", "--action", required=True, choices=sorted(ACTIONS.keys()))
    parser.add_argument("-m", "--model", required=True, choices=sorted(MODEL_MAP.keys()))
    parser.add_argument("--id", type=int)
    parser.add_argument("-n", "--name", type=str)
    parser.add_argument("--group-id", type=int)
    parser.add_argument("--teacher-id", type=int)
    parser.add_argument("--student-id", type=int)
    parser.add_argument("--subject-id", type=int)
    parser.add_argument("--grade", type=float)
    parser.add_argument("--date", type=str, help="YYYY-MM-DD")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    ACTIONS[args.action](args.model, args)


if __name__ == "__main__":
    main()
