import ast
import copy
import types

from bs4 import BeautifulSoup

from analyzer.registered_plugins import registered_plugins
from vulnerability.vulnerability import Vulnerability
from vulnerability.vulnerabilities_config import sqlstrformat, xssstrformat


def check_for_sqli(format_str):
    format_str = format_str.upper()
    sql_strings = ["INSERT INTO", "DELETE FROM", "CREATE TABLE", "ALTER TABLE", "DROP TABLE", "TRUNCATE TABLE",
                   "DROP DATABASE", "CREATE DATABASE", "CREATE TRIGGER", "DROP TRIGGER", "CREATE VIEW", "DROP VIEW"]
    sql_tuples = [("SELECT", "FROM"), ("UPDATE", "SET")]  # These need to be in sequence
    if any(sql_str in format_str for sql_str in sql_strings):
        return True
    for sql_tuple in sql_tuples:
        index0 = format_str.find(sql_tuple[0])
        if index0 != -1:
            if format_str.find(sql_tuple[1], index0 + len(sql_tuple[0])) != -1:
                return True
    return False


def check_for_xss(format_str):
    format_str = format_str.lower()
    # try to parse the string to html to check if it is html
    if bool(BeautifulSoup(format_str, "html.parser").find()):
        return True
    else:
        return False


class Analyzer(ast.NodeVisitor):

    def create_visitor_functions(self):
        for node_type in registered_plugins:
            def func(instance, node):
                for reg_plugin in registered_plugins[type(node).__name__]:
                    registered_plugins[type(node).__name__][reg_plugin](instance, node)
                instance.generic_visit(node)
            exec("Analyzer.visit_%s = copy.deepcopy(func)" % node_type)
            del func

    def __init__(self, file):
        self.used_libraries = []
        self.vulnerabilities = set([])
        self.file = file
        self.create_visitor_functions()

    def check_for_inj(self, format_string, node):
        if check_for_sqli(format_string):
            self.vulnerabilities.add(Vulnerability(file=self.file, lineno=node.lineno,
                                                      vuln_type=sqlstrformat))
        if check_for_xss(format_string):
            self.vulnerabilities.add(Vulnerability(file=self.file, lineno=node.lineno,
                                                      vuln_type=xssstrformat))

    def visit_Import(self, node):
        """
        Appends all used libraries e. g. requirements to self.used_libraries
        :param node: The Import node
        :return: None
        """
        for alias in node.names:
            if alias not in self.used_libraries:
                self.used_libraries.append(alias.name)
        self.generic_visit(node)  # calls visit() on all children

    def visit_ImportFrom(self, node):
        """
        Appends all used libraries e. g. requirements to self.used_libraries
        :param node: The ImportFrom node
        :return: None
        """
        if node.module not in self.used_libraries:
            self.used_libraries.append(node.module)
        self.generic_visit(node)

    def visit_JoinedStr(self, node):
        format_string = ""
        for val in node.values:
            if isinstance(val, ast.Constant):
                if isinstance(val.value, str):
                    format_string += val.value
        self.check_for_inj(format_string, node)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if node.attr == "format":
            self.check_for_inj(node.value.value, node)
        self.generic_visit(node)

    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Mod):  # Modulo operator used for string formatting like "hello %s" % x
            if isinstance(node.left, ast.Constant):  # left side is string constant
                if "%s" in node.left.value:  # %d, %f are not receptive to injection as they only accept numbers
                    self.check_for_inj(node.left.value, node)
        # if isinstance(node.op, ast.Add):
        #     if isinstance(node.right, ast.Constant):
        #         if isinstance(node.right.value, str):
        self.generic_visit(node)

    def report(self):
        for vulnerability in self.vulnerabilities:
            print(vulnerability)
        if self.vulnerabilities:
            print("----------------------")
        return self.vulnerabilities


