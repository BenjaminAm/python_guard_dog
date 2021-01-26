import ast
from analyzer.plugin_loader import registered_plugins


class Analyzer(ast.NodeVisitor):

    def create_visitor_functions(self):
        for node_type in registered_plugins:
            def func(instance, node):
                for reg_plugin in registered_plugins[type(node).__name__]:
                    registered_plugins[type(node).__name__][reg_plugin]\
                        (instance, node)
                instance.generic_visit(node)
            setattr(Analyzer, "visit_%s" % node_type, func)

    def __init__(self, file):
        self.used_libraries = []
        self.vulnerabilities = set([])
        self.file = file
        self.create_visitor_functions()

    def report(self):
        for vulnerability in self.vulnerabilities:
            print(vulnerability)
        if self.vulnerabilities:
            print("----------------------")
        return self.vulnerabilities


