from datetime import date
from create import Office, Agent, Listing, Buyer, Sale, engine, Base
from sqlalchemy.orm import sessionmaker

# start the session to insert data into the database
Session = sessionmaker(bind=engine)
session = Session()

# insert initial data for office, real estate agent, listings and buyers information
offices = [
    Office(officename = 'East Village'),
    Office(officename = 'Upper East Side')
]

agents = [
    Agent(officeid=2,firstname = 'Jenny',lastname='Smith',phone='415-2134455',email='jenny.smith@realestate.com'),
    Agent(officeid=1,firstname = 'Thomas',lastname='Davidson',phone='213-76334877',email='thomas@realestate.com'),
    Agent(officeid=1,firstname = 'Allison',lastname='Chung',phone='763-5231455',email='achung@realestate.com'),
    Agent(officeid=2,firstname = 'Albert',lastname='Saul',phone='623-5122731',email='albert.saul@realestate.com'),
]

eastVillageListings = [
    Listing(listingname='1 bedroom in East Village', bedroom_no=1, bathroom_no=1, address='431 1st Ave, New York', zipcode='10009', listing_price=185700.00, listing_date=date(2022,3,15), listing_month=202203, listing_agent=2, listing_office=1),
    Listing(listingname='2 bedrooms in Kips Bay', bedroom_no=2, bathroom_no=1, address='38 E 28th Street , New York', zipcode='10016', listing_price=235000.00, listing_date=date(2021,10,12), listing_month=202110, listing_agent=3, listing_office=1),
    Listing(listingname='Unit 4C 101 East 2nd Street', bedroom_no=3, bathroom_no=2, address='101 East 2nd Street, New York', zipcode='10009', listing_price=865000.00, listing_date=date(2022,4,3), listing_month=202204, listing_agent=2, listing_office=1),
    Listing(listingname='Cozy 1 bedroom apartment in East Village', bedroom_no=1, bathroom_no=1, address='414 East 10th Street, New York', zipcode='10009', listing_price=315000.00, listing_date=date(2022,4,1), listing_month=202204, listing_agent=3, listing_office=1),
    Listing(listingname='Two bedroom apartment in East Village', bedroom_no=2, bathroom_no=2, address='268 East 4th Street, New York', zipcode='10009', listing_price=489000.00, listing_date=date(2022,3,12), listing_month=202203, listing_agent=2, listing_office=1),
    Listing(listingname='Four bedroom Condo', bedroom_no=4, bathroom_no=2, address='383 East 10th Street, New York', zipcode='10009', listing_price=1325000.00, listing_date=date(2022,2,10), listing_month=202202, listing_agent=2, listing_office=1),
    Listing(listingname='Glamorous 4 bedroom condo', bedroom_no=4, bathroom_no=2, address='149 Avenue C, New York', zipcode='10009', listing_price=599000.00, listing_date=date(2022,2,23), listing_month=202202, listing_agent=3, listing_office=1),
    Listing(listingname='Rustic 3 bedroom apartment', bedroom_no=3, bathroom_no=1, address='633 East 11th Street, New York', zipcode='10009', listing_price=365000.00, listing_date=date(2022,1,10), listing_month=202201, listing_agent=2, listing_office=1),
]

uesListings = [
    Listing(listingname='3 bedroom with nice city views', bedroom_no=3, bathroom_no=1, address='345 East 93rd Street, New York', zipcode='10128', listing_price=65900.00, listing_date=date(2022,2,10), listing_month=202202, listing_agent=1, listing_office=2),
    Listing(listingname='Luxurious condo in Upper East Side', bedroom_no=4, bathroom_no=2, address='340 East 80th Street, New York', zipcode='10075', listing_price=169500.00, listing_date=date(2022,2,28), listing_month=202202, listing_agent=4, listing_office=2),
    Listing(listingname='Luxurious condo in Park Avenue', bedroom_no=5, bathroom_no=3, address='925 Park Avenue, New York', zipcode='10028', listing_price=3300000.00, listing_date=date(2022,3,15), listing_month=202203, listing_agent=4, listing_office=2),
    Listing(listingname='Family-friendly apartment in Upper East Side', bedroom_no=5, bathroom_no=2, address='8 East 83rd Street, New York', zipcode='10028', listing_price=1695000.00, listing_date=date(2022,3,20), listing_month=202203, listing_agent=1, listing_office=2),
    Listing(listingname='Affordable 3 bedroom apartment for young people', bedroom_no=3, bathroom_no=1, address='448 East 84th Street, New York', zipcode='10028', listing_price=425000.00, listing_date=date(2022,1,15), listing_month=202201, listing_agent=4, listing_office=2),
    Listing(listingname='Artistic 3 bedroom condo', bedroom_no=3, bathroom_no=3, address='420 East 72nd Street, New York', zipcode='10028', listing_price=2100000.00, listing_date=date(2022,4,1), listing_month=202204, listing_agent=1, listing_office=2),
    Listing(listingname='Triple Duplex on Park Avenue', bedroom_no=5, bathroom_no=3, address='730 Park Avenue, New York', zipcode='10021', listing_price=35000000.00, listing_date=date(2022,1,23), listing_month=202201, listing_agent=1, listing_office=2),
]

buyers = [
    Buyer(firstname='Alice',lastname='Liberman',email='alice@gmail.com',phone='213-4132566'),
    Buyer(firstname='Cody',lastname='Simpson',email='csimpson@gmail.com',phone='412-5634155'),
    Buyer(firstname='Daniel',lastname='Chang',email='daniel.chang@gmail.com',phone='617-4223587'),
    Buyer(firstname='Frank',lastname='Soderman',email='frank@gmail.com',phone='567-7123455'),
    Buyer(firstname='George',lastname='Peters',email='george.peters@gmail.com',phone='719-5234612'),
]

session.add_all(offices)
session.add_all(agents)
session.add_all(eastVillageListings)
session.add_all(uesListings)
session.add_all(buyers)
session.commit()

# Package a sales into a 'transaction' function that can update both Sales and Listing tables at the same time
def add_sales(buyer, listing, price, date_list, month, agent):
    try:
        sale = Sale(buyerid=buyer,listingid=listing,sales_price=price,sales_date=date(date_list[0],date_list[1],date_list[2]), sales_month = month, agentid=agent)
        session.add(sale)
        sale_listing = session.query(Listing).get(listing)
        sale_listing.sold = True
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

add_sales(1,1,200000,(2022,3,28),202203,1)
add_sales(2,4,350000,(2022,3,15),202203,2)


