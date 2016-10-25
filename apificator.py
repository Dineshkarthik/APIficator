"""Tornado App to Generate Rest API for existing Database."""
import sys
import tornado.escape
import tornado.ioloop
import tornado.web
import json
from sqlalchemy import *
import psycopg2
import MySQLdb
import pyodbc
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import *


class AbsShardingClass(Base):
    """Abstract class used to create dynamic classes for DB tables."""

    __abstract__ = True


def get_class_name_and_table_name(hashid):
    """Return class & table name."""
    return 'ShardingClass%s' % hashid, '%s' % hashid


def get_sharding_entity_class(hashid):
    """Generate dynamic classes for DB tables."""
    class_name, table_name = get_class_name_and_table_name(hashid)
    cls = type(class_name, (AbsShardingClass, ), {'__tablename__': table_name})
    return cls


def new_alchemy_encoder():
    """Function to convert sqlalchemy results to json."""
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj)
                              if not x.startswith('_') and x != 'metadata']:
                    fields[field] = obj.__getattribute__(field)
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


db = create_engine(sys.argv[1], echo=False)
Base = declarative_base()
Base.metadata.reflect(db)
Session = sessionmaker(bind=db)
session = Session()

tables = db.table_names()
ar = []

if __name__ == "__main__":
    application.listen(8800)
    print("* Running on http://127.0.0.1:8800/")
    tornado.ioloop.IOLoop.instance().start()
