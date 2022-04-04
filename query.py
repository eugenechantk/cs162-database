from create import Office, Agent, Listing, Buyer, Sale, engine, Base
from sqlalchemy.orm import sessionmaker

# start the session to query data into the database
Session = sessionmaker(bind=engine)
session = Session()

