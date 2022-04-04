from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from query import Office

# establish the connection to the database created from create.py
engine = create_engine('sqlite:///realestate.db', echo=True)
Base = declarative_base(engine)

# start the session to insert data into the database
Session = sessionmaker(bind=engine)
session = Session()

