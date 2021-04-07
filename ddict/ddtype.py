# Data Dictionary Type
from os import path
import re
import yaml
from jinja2 import Environment, Undefined

REMOVELINE = '<RemoveLine>'

class DdUndefined(Undefined):
    def __str__(self):
        # Undefined Variables will emit this instead of None
        # so that we can find lines to remove later
        return REMOVELINE

class DdType(object):
    def __init__(self):
        with open(path.join('..', path.join('shared', 'types.yml'))) as fh:
            doc = yaml.load(fh, Loader=yaml.Loader) 

        self.env = Environment(undefined=DdUndefined)
        self.schema = doc.get('schema')
        self.base_types = doc.get('base_types')
        self.ddltpl = self.env.from_string(doc.get('ddl'))
        self.custom_types = doc.get('custom_types')
    def genddl(self):
        # uses jinja2 to generate DDL for custom types
        pg = re.compile(REMOVELINE)
        ddl = ''
        for ct in self.custom_types:
            rawddl = '-- DDL for ' + ct.get('name') + "\n"
            ct['schema'] = self.schema
            rawddl += self.ddltpl.render(ct)
            # Remove all lines with undefined vars
            for line in rawddl.splitlines():
                if not pg.search(line):
                    ddl += line + "\n"
            ddl += ";\n"
        return ddl

if __name__ == '__main__':
    ddt = DdType()
    print(ddt.genddl())
