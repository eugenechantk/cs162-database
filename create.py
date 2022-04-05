import sqlalchemy
from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey, Date, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# establish connection to the database
# if database does not exist, create a new one
# echo=True to see the SQL commands and run time
engine = create_engine('sqlite:///realestate.db', echo=True)
engine.connect()

# provide the base for declarative method to create tables
Base = declarative_base()

class Office(Base):
    __tablename__ = 'office'
    officeid = Column(Integer, primary_key=True)
    officename = Column(Text)
    listings = relationship("Listing")
    agents = relationship("Agent")

    def __repr__(self):
        return "<Office(ID={}, Office Name={})>".format(self.officeid, self.officename)


class Agent(Base):
    __tablename__ = 'agent'
    agentid = Column(Integer, primary_key=True)
    officeid = Column(Integer,ForeignKey('office.officeid'))
    firstname = Column(Text)
    lastname = Column(Text)
    phone = Column(Text)
    email = Column(Text)
    listings = relationship("Listing")
    sales = relationship("Sale")

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
    sales = relationship("Sale")

    def __repr__(self):
        return "<Listing(ID={}, Name={}, Listing Price={}, Listing Date={}, Listing Agent={}, Listing Office={})>".format(self.listingid, self.listingname, self.listing_price, self.listing_date, self.listing_agent, self.listing_office)

class Buyer(Base):
    __tablename__ = 'buyer'
    buyerid = Column(Integer, primary_key=True)
    firstname = Column(Text)
    lastname = Column(Text)
    email = Column(Text)
    phone = Column(Text)
    sales = relationship("Sale")

# provide a utility function to calculate the comission
def calc_comission(context):
    sales_price = context.get_current_parameters()['sales_price']
    if sales_price < 100000.00:
        return sales_price*0.1
    if sales_price <= 200000.00:
        return sales_price*0.075
    if sales_price <= 500000.00:
        return sales_price*0.06
    if sales_price <= 1000000.00:
        return sales_price*0.05
    return sales_price*0.04 

class Sale(Base):
    __tablename__ = 'sale'
    saleid = Column(Integer, primary_key=True)
    buyerid = Column(Integer, ForeignKey('buyer.buyerid'))
    listingid = Column(Integer, ForeignKey('listing.listingid'))
    sales_price = Column(Float)
    sales_date = Column(Date)
    sales_month = Column(Integer)
    agentid = Column(Integer, ForeignKey('agent.agentid'))
    comission = Column(Float, default=calc_comission, onupdate=calc_comission) # utilize default and onupdate to insert and update comission data based on sales price

class Commission(Base):
    __tablename__ = 'commission'
    commissionid = Column(Integer, primary_key=True)
    agentid = Column(Integer, ForeignKey('agent.agentid'))
    commission = Column(Float)
    commission_month = Column(Integer)


# create all the tables defined above 
Base.metadata.create_all(bind=engine)

'''
Data Normalization Check
1NF:
- Each attribute in each table only takes in 1 value, and their domains don't change
- Each attribute has a unique name within the table scope
- The order in which data is stored does not matter

2NF:
- All other attributes in each table is dependent on the primary key (i.e. the ids)

3NF
- There is no non-primary-key attribute that depends beyond the primary key of its own table, therefore no transitive dependencies
- e.g. lastname of agent is not dependent on firstname of agent, just agentid of agent
'''