import sqlalchemy
from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey, Date, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///realestate.db')
engine.connect()

Base = declarative_base()

class Office(Base):
    __tablename__ = 'office'
    officeid = Column(Integer, primary_key=True)
    officename = Column(Text)
    listings = relationship("Listing")

    def __repr__(self):
        return "<Office(ID={}, Office Name={})>".format(self.officeid, self.officename)


class Agent(Base):
    __tablename__ = 'agent'
    agentid = Column(Integer, primary_key=True)
    firstname = Column(Text)
    lastname = Column(Text)
    phone = Column(Text)
    email = Column(Text)
    listings = relationship("Listing")

    def __repr__(self):
        return "<Agent(ID={}, Name={} {}, Phone={}, Email={})>".format(self.agentid, self.firstname, self.lastname, self.phone, self.email)

class Listing(Base):
    __tablename__ = 'listing'
    listingid = Column(Integer, primary_key=True)
    listingname = Column(Text)
    bedroom_no = Column(Integer)
    bathroom_no = Column(Integer)
    # ammenities = Column(Text) # store the text version of a JSON object that describes ammenities for the house
    address = Column(Text)
    zipcode = Column(Text)
    listing_price = Column(Float)
    listing_date = Column(Date)
    listing_month = Column(Integer)
    listing_agent = Column(Integer, ForeignKey('agent.agentid'))
    listing_office = Column(Integer, ForeignKey('office.officeid'))
    sold = Column(Boolean, default=False)

    def __repr__(self):
        return "<Listing(ID={}, Name={}, Listing Price={}, Listing Date={}, Listing Agent={}, Listing Office={})>".format(self.listingid, self.listingname, self.listing_price, self.listing_date, self.listing_agent, self.listing_office)
    
class Sale(Base):
    __tablename__ = 'sale'
    saleid = Column(Integer, primary_key=True)
    buyerid = Column(Integer, ForeignKey('buyer.buyerid'))
    listingid = Column(Integer, ForeignKey('listing.listingid'))
    sales_price = Column(Float)
    sales_date = Column(Date)
    sales_month = Column(Integer)
    agentid = Column(Integer, ForeignKey('agent.agentid'))

class Buyer(Base):
    __tablename__ = 'buyer'
    buyerid = Column(Integer, primary_key=True)
    firstname = Column(Text)
    lastname = Column(Text)
    email = Column(Text)
    phone = Column(Text)

Base.metadata.create_all(bind=engine)
