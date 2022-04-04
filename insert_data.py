from curses import echo
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///realestate.db', echo=True)
Base = declarative_base(engine)

class Office(Base):
    __tablename__ = 'office'
    __table_args__ = {'autoload': True}

class Agent(Base):
    __tablename__ = 'agent'
    __table_args__ = {'autoload': True}

class Listing(Base):
    __tablename__ = 'listing'
    __table_args__ = {'autoload': True}

class Sale(Base):
    __tablename__ = 'sale'
    __table_args__ = {'autoload': True}

class Buyer(Base):
    __tablename__ = 'buyer'
    __table_args__ = {'autoload': True}

metadata = Base.metadata
Session = sessionmaker(bind=engine)
session = Session()

newOffice = Office(officename='testing')
session.add(newOffice)
session.commit()