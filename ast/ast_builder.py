import ast
import os
from pprint import pprint


def build_ast(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return ast.parse(f.read())
    raise IOError('Input needs to be a file. Path: ' + path)


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": []}

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["import"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["from"].append(alias.name)
        self.generic_visit(node)

    def report(self):
        pprint(self.stats)

