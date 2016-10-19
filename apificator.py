"""Tornado App to Generate Rest API for existing Database."""
import sys
import string
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


class ApiGenerator:
    """Class used to generate code for API on the fly."""

    def begin(self, tab="\t"):
        self.code = []
        self.tab = tab
        self.level = 0

    def end(self):
        return string.join(self.code, "")

    def write(self, string):
        self.code.append(self.tab * self.level + string)

    def indent(self):
        self.level = self.level + 1

    def dedent(self):
        if self.level == 0:
            raise SyntaxError, "internal error in code generator"
        self.level = self.level - 1

    def newline(self, no=1):
        res = ""
        i = 1
        while (i <= no):
            res += "\n"
            i += 1
        self.code.append(res)


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
session = create_session(bind=db)

tables = db.table_names()
ar = []

c = ApiGenerator()
c.begin(tab="    ")
for t in tables:
    c1 = ApiGenerator()
    c1.begin(tab="    ")
    c1.write("class " + t + "(Base):\n")
    c1.indent()
    c1.write("__table__ = Base.metadata.tables['" + t + "']")
    c1.dedent()
    c1.newline(no=2)
    exec (c1.end())
    key = inspect(eval(t)).primary_key[0].key
    c.write("class " + t + "Details" + "(tornado.web.RequestHandler):\n")
    c.indent()
    c.write("def get(self):\n")
    c.indent()
    c.write("args = self.request.arguments\n")
    c.write("if args:\n")
    c.indent()
    c.write("a = []\n")
    c.write("t = '" + t + "'\n")
    c.write("for k, v in args.iteritems():\n")
    c.indent()
    c.write("""a.append(" " + t + "." + k + "='" + v[0] + "'")\n""")
    c.dedent()
    c.write("""result = session.query(""" + t + """).filter(
                    (','.join(a).replace(",", "AND"))).all()\n""")
    c.dedent()
    c.write("else:\n")
    c.indent()
    c.write("p_id = (self.request.uri).rsplit('/', 1)[1]\n")
    c.write("if p_id:\n")
    c.indent()
    c.write("""result = session.query(""" + t + """).filter_by(""" + key +
            """=p_id).first()\n""")
    c.dedent()
    c.write("else:\n")
    c.indent()
    c.write("""result = session.query(""" + t + """).all()\n""")
    c.dedent()
    c.dedent()
    c.write("""self.set_header(
                "Content-Type", 'application/json; charset="utf-8"')\n""")
    c.write("""self.write(json.dumps(
                result, cls=new_alchemy_encoder(), check_circular=False))""")
    c.dedent()
    c.dedent()
    c.newline(no=2)
    ar.append('(r"/' + t + "/?" '", ' + t + 'Details)')
    ar.append('(r"/' + t + "/[a-zA-Z0-9]+" '", ' + t + 'Details)')
c.write("application = tornado.web.Application([" + ','.join(ar) + "])")
exec (c.end())

if __name__ == "__main__":
    application.listen(8800)
    print("* Running on http://127.0.0.1:8800/")
    tornado.ioloop.IOLoop.instance().start()
