import ast
import os


def build_ast(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return ast.parse(f.read())
    raise IOError('Input needs to be a file. Path: ' + path)
