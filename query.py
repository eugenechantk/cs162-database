from create import Office, Agent, Listing, Buyer, Sale, Commission, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, insert, select
from sqlalchemy.schema import Index

# start the session to query data into the database
Session = sessionmaker(bind=engine)
session = Session()

# utility function for printing results
def print_result(results):
    for result in results:
        print (result)

report_month = 202203 # specifying the month to build the report

# Q1. find top 5 offices with the most sales for that month
Index('idx_agent_to_price',Sale.agentid, Sale.sales_price) # composite index to facilitate grouping sales price by agent
Index('idx_agent_to_office',Agent.agentid,Agent.officeid) # composite index to facilitate grouping office by agent
top_office_sales = session.query(
    Office.officename,
    func.sum(Sale.sales_price)
).\
    join(Agent,Sale.agentid==Agent.agentid).\
    join(Office,Agent.officeid==Office.officeid).\
    group_by(Office.officeid).\
    order_by(func.sum(Sale.sales_price).desc()).\
    limit(5)

print('Top 5 office by sales:')
print_result(top_office_sales)
print('==========================\n')

# Q2. top 5 agents with the most sales (inc. contact details)
top_agent = session.query(
    Agent.firstname,
    Agent.lastname,
    Agent.email,
    Agent.phone,
    func.sum(Sale.sales_price)
).\
    join(Agent,Sale.agentid == Agent.agentid).\
    group_by(Agent.agentid).\
    order_by(func.sum(Sale.sales_price).desc()).\
    limit(5)

print('Top 5 real estate agent by sales:')
print_result(top_agent)
print('==========================\n')

# Q3a. calculate commission for each agent and store in separate table
Index('idx_agent_sales',Sale.agentid) # Index to facilitate group by agent
commission = session.query(
    Sale.agentid,
    func.sum(Sale.comission),
    Sale.sales_month
).filter(Sale.sales_month==report_month).group_by(Sale.agentid)

i = insert(Commission).from_select(['agentid','commission','commission_month'],select=commission)
session.execute(i)
session.commit()

Index('idx_agent_agent', Agent.agentid) # Index to facilitate joining agent for the query on Commission table below
commission_by_agent = session.query(
    Agent.firstname,
    Agent.lastname,
    Commission.commission
).filter(Commission.commission_month == report_month).join(Agent,Commission.agentid == Agent.agentid)

print('Commission by agent:')
print_result(commission_by_agent)
print('==========================\n')

# Q3b. Number of days on the market
days_on_market = session.query(
    func.avg(func.julianday(Sale.sales_date)-func.julianday(Listing.listing_date))
).filter(Sale.sales_month == report_month).join(Listing,Sale.listingid == Listing.listingid)

print(f'Average lead time for houses sold this month: {days_on_market[0][0]:.0f} days')
print('==========================\n')

# Q4. Average selling price
average_selling_price = session.query(
    func.avg(Sale.sales_price)
).filter(Sale.sales_month == report_month)

print(f'Average sale price for houses sold this month: ${average_selling_price[0][0]:.2f}')
print('==========================\n')