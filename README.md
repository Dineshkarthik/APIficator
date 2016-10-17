# APIficator

Would you like to expose an existing database via REST API? Normally, you'd have to write a lot of code for the ORM you're using, then integrate that into some web framework. 

`APIficator` does the coding part for you, you can generate API services without writing any code.

##### All you need to do:
  - Enter the requirements in the YAML file
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

Configuring YAML
------------------

Open `conf.yaml` file, the basic structure is as follows
```sh
DB: sqlite:///mydatabase.db

API:
  user:
    url: /
    query: "select * from users;"
    method: get

  place:
    url: /place
    query: "select * from place;"
    method: get
```

* `DB`: The DB Connection URl for your respective DB.
* All the configurations related to APIs are defined under `API`.
* `user`, `places` in the agove yaml is the seperator key which is user defined.
* `url`: it is the URL in which the particular API service will the avilable.
* `query`: the SQL query for which you need the result, the same will be served in the API.
* `method`: get, post, patch, put, delete. Specify the method

##### NOTE:
> In the current version of APIficator only get and post methods are implemented without any arguments for filtering. These features will be added in the upcoming versions.


### Installation

You need Python, its dependency packages,  Tornado, SQLAlchemy and pandas installed globally:

```sh
$ git clone https://github.com/Dineshkarthik/APIficator.git
$ cd APIficator
$ pip install -r requirements.txt
$ python apificator.py
```

> By default the application runs in the port `8800`. Can be accessed as `http://localhost:8800`

License
----

MIT


**Free Software, Hell Yeah!**
