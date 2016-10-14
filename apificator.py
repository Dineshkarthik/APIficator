"""Tornado App to Generate Rest API for existing Database."""
import sys
import string
import yaml
import tornado.escape
import tornado.ioloop
import tornado.web
import json
from sqlalchemy import *


class ApiGenerator:
    """Class used to generate code for API on the fly"""
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


with open('conf.yaml', 'r') as f:
    conf = yaml.load(f)

db = create_engine(conf["DB"], echo=False)
connection = db.connect()

c = ApiGenerator()
c.begin(tab="    ")

ar = []
for key in conf["API"]:
    c.write("class " + conf["API"][key]["class"] +
            "(tornado.web.RequestHandler):\n")
    c.indent()
    c.write("def " + conf["API"][key]["method"] + "(self):\n")
    c.indent()
    c.write("rs = connection.execute('" + conf["API"][key]["query"] + "')\n")
    c.write(
        """self.set_header("Content-Type", 'application/json; charset="utf-8"')\n""")
    c.write("self.write(json.dumps([(dict(row.items())) for row in rs]))\n\n")
    ar.append('(r"' + conf["API"][key]["url"] + '", ' + conf["API"][key][
        "class"] + ')')
    c.dedent()
    c.dedent()
c.newline(no=2)
c.write("application = tornado.web.Application([" + ','.join(ar) + "])")
exec(c.end())

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
