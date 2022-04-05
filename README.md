# Real Estate Head Office Database
## Running the database
```
python3.6 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 create.py
python3 insert_data.py
python3 query_data.py
```
## LO/HC appendix
`#cs162-communication`: I have commited my code in small increments, each containing only a functionality. I have written clear and concise commit messages for each commit to explain what has changed. I have also written extensive comment in the code and in my pull request to explain my implementation.  
`#cs162-sql`: In this assignment, I chose to use an ORM (i.e. SQLAlchemy) to construct the manipulate with the database because the syntax is more familiar to me (i.e. Python and OOP).  
I have implemented data normalization to make sure data is not redundant and is not dependent through complex relationships.  
In the implementation of queries, I utilized indexes to speed up SQL operations. It resulted in faster runtime (i.e. when running the first query, the time got shorten by 17% -- can check by commenting out the Index commands).  
To reflect a sales in the database, because we need to update multiple tables, to maintain integrity of the database, I implemented a function that essentially wraps the SQL commands into a transaction, with rollback to ensure that we can revert if the transaction is faulty.  
