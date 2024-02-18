from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:myPass@localhost:5432/university")
DBSession = sessionmaker(bind=engine)
session = DBSession()
