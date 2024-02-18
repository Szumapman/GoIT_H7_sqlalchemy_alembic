from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://myUser:myPass@localhost:5432/university")
DBSession = sessionmaker(bind=engine)
session = DBSession()
