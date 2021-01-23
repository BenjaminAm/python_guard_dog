import ast
from analyzer.plugin_loader import registered_plugins


class Analyzer(ast.NodeVisitor):

    def create_visitor_functions(self):
        for node_type in registered_plugins:
            def func(instance, node):
                for reg_plugin in registered_plugins[type(node).__name__]:
                    registered_plugins[type(node).__name__][reg_plugin](instance, node)
                instance.generic_visit(node)
            exec("Analyzer.visit_%s = func" % node_type)

    def __init__(self, file):
        self.used_libraries = []
        self.vulnerabilities = set([])
        self.file = file
        self.create_visitor_functions()

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

    def report(self):
        for vulnerability in self.vulnerabilities:
            print(vulnerability)
        if self.vulnerabilities:
            print("----------------------")
        return self.vulnerabilities


