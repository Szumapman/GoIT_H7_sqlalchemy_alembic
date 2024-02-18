from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_session import session


# engine = create_engine("postgresql://postgres:mysec@localhost:5432/postgres")
# DBSession = sessionmaker(bind=engine)
# session = DBSession()


def create(model, **kwargs):
    new_object = model(**kwargs)
    session.add(new_object)
    session.commit()


def read(model, required_args, **kwargs):
    if kwargs:
        objects = session.query(model).filter_by(**kwargs).all()
    else:
        objects = session.query(model).all()
    for pulled_object in objects:
        for field_name in required_args:
            if isinstance(
                getattr(pulled_object, field_name), (str, int, float, datetime)
            ):
                print(
                    f"{field_name} : {getattr(pulled_object, field_name)}",
                    end=" ",
                )
        print()


def update(model, **kwargs):
    if "id" in kwargs:
        pulled_object = session.get(model, kwargs["id"])
        for attribute, new_value in kwargs.items():
            if attribute != "id":
                setattr(pulled_object, attribute, new_value)
        session.add(pulled_object)
        session.commit()
    else:
        print("For update you must specify --id argument.")


def delete(model, **kwargs):
    if "id" in kwargs:
        pulled_object = session.get(model, kwargs["id"])
        session.delete(pulled_object)
        session.commit()
    else:
        print("For delete you must specify --id argument.")
