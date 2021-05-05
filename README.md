Description:
Class and script for parsing sites in multi-threaded mode


Files description (script):
SpiderClass.py - Class for parse and connection with DB
index.py - main script that executes parsing
spider.sql - SQL-code

Required modules:
- mysql.connector
- requests
- re
- BeautifulSoup
- time
- concurrent.futures
- datetime

To-do:
- install mysql
- create DB mysql (default name - "spider")
- import spider.sql
- index.py, lines 5-8 - write a data for connection to DB
- index.py, line 9 - write a site that you need to parse
- index.py, line 10 - write symbols or words that parser should avoid
- run index.py

Additionally:
Parser uses 30 streams by default. Write the amount of streams you need in index.py, line 11
