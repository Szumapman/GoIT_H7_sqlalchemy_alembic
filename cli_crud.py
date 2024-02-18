import argparse
import inspect
from datetime import datetime

from crud import create, read, update, delete
from models import Group, Student, Lecturer, Course, Grade


def get_required_args(cls):
    cls_args = [
        name
        for name, value in inspect.getmembers(cls)
        if not name.startswith(
            (
                "__",
                "_",
                "metadata",
                "registry",
            )
        )
    ]
    return cls_args


def passed_args(required_args, **kwargs):
    kwargs = {
        key: value for key, value in kwargs.items() if key in required_args and value
    }
    if "date_of" in kwargs:
        kwargs["date_of"] = datetime.strptime(kwargs["date_of"], "%d-%m-%Y").date()
    return kwargs


def set_parsed_args():
    parser = argparse.ArgumentParser(description="Seed database")
    parser.add_argument(
        "--action",
        "-a",
        choices=["create", "list", "update", "remove"],
        required=True,
        help="CRUD action",
    )
    parser.add_argument(
        "--model",
        "-m",
        choices=[
            "Group",
            "Lecturer",
            "Student",
            "Course",
            "Grade",
        ],
        required=True,
        help="Model name",
    )
    parser.add_argument("--id", type=int, help="ID required for update and remove")
    parser.add_argument("--group_name", help="Group name")
    parser.add_argument("--student_name", help="Student name")
    parser.add_argument("--lecturer_name", help="Lecturer name")
    parser.add_argument("--course_name", help="Course name")
    parser.add_argument("--lecturer_id", type=int, help="Lecturer ID")
    parser.add_argument(
        "--grade", type=float, help="Grade from scope: 2, 2.5, 3, 3.5, 4, 4.5, 5"
    )
    parser.add_argument("--group_id", type=int, help="Group ID")
    parser.add_argument("--email", help="Email - must be unique")
    parser.add_argument(
        "--date_of", type=str, help="Date of in the format: %d-%m-%Y e.g.: 31-01-2024"
    )
    parser.add_argument("--course_id", type=int, help="Course ID")
    parser.add_argument("--student_id", type=int, help="Student ID")
    return parser.parse_args()


if __name__ == "__main__":
    args = set_parsed_args()
    model = globals()[args.model]
    required_args = get_required_args(model)
    kwargs = passed_args(required_args, **vars(args))

    if args.action == "create":
        create(model, **kwargs)
    elif args.action == "list":
        read(model, required_args, **kwargs)
    elif args.action == "update":
        update(model, **kwargs)
    elif args.action == "remove":
        delete(model, **kwargs)
    else:
        print("No action specified")
