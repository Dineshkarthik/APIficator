# APIficator

Would you like to expose an existing database via REST API? Normally, you'd have to write a lot of code for the ORM you're using, then integrate that into some web framework. 

`APIficator` does the coding part for you, you can generate API services without writing any code.

##### All you need to do:
  - Run the python app
  - The app will generate and launch REST API service for you
 

Supported Databases
------------------

`APIficator`, by default, supports connections to the same set of databases as
[SQLAlchemy](http://www.sqlalchemy.org). As of this writing, that includes:

* MySQL (MariaDB)
* PostgreSQL
* SQLite
* Oracle
* Microsoft SQL Server
* Firebird
* Drizzle
* Sybase
* IBM DB2
* SAP Sybase SQL Anywhere
* MonetDB

Database Urls
-------------
* SQLite - `sqlite:///database_name.db`
* PostgreSQL - `postgresql+psycopg2://user_name:password@localhost/mydatabase`
* MySQL - `mysql+mysqldb://user_name:password@localhost/database`
* Oracle - `oracle://user_name:password@127.0.0.1:1521/sidname`
* Microsoft SQL Server - `mssql+pyodbc://user_name:password@mydsn`

### Installation

You need Python, its dependency packages,  Tornado, SQLAlchemy and pandas installed globally:

```sh
$ git clone https://github.com/Dineshkarthik/APIficator.git
$ cd APIficator
$ pip install -r requirements.txt
$ python apificator.py [Database Url]

Example:
$ python apificator.py sqlite:///database_name.db
```

### Filtering and Sorting
**You don't even need to specify what are the tables present in your database.** 
 Just point at your database and let `APIficator` do all the heavy lifting

Let's see the awesome filtering capability of APIficator:

When filtering with ***Primary key*** add the primary key at the end of the URL as below:
```sh
> python apificator.py sqlite:///database_name.db
* Running on http://127.0.0.1:8800/

> curl GET "http://localhost:8800/users/1"
```

```json
...
{
    "UserId": 1,
    "Name": "Bob",
    "Age": 24,
    "Gender": "Male"
}
```

When filtering with columns other then primary key of the table pass the values as params with `column name` as  param key, as below:
```sh
> python apificator.py sqlite:///database_name.db
* Running on http://127.0.0.1:8800/

> curl GET "http://localhost:8800/users/?Gender=Female&Name=Lynda"
```

```json
...
{
    "UserId": 21,
    "Name": "Lynda",
    "Age": 43,
    "Gender": "Female"
}
```

##### NOTE:
> In the current version of APIficator only generaters APIs for get method. API service for other REST methods will be added in the upcoming versions.


License
----

MIT


**Free Software, Hell Yeah!**
