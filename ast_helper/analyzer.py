import ast


class Analyzer(ast.NodeVisitor):
    def __init__(self, file):
        self.used_libraries = []
        self.vulnerabilities = []
        self.file = file

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
        return self.vulnerabilities


