import types
from .analyzer import Analyzer
from .registered_plugins import registered_settings_plugins
from vulnerability.vulnerability import Vulnerability
from vulnerability.vulnerabilities_config import djdebug, djcsrfmidw, djsecmidw


class SettingsAnalyzer(Analyzer):
    def create_visitor_functions(self):
        for node_type in registered_settings_plugins:
            def func(instance, node):
                for reg_plugin in registered_settings_plugins[node_type]:
                    registered_settings_plugins[node_type][reg_plugin](instance, node)
                    print(registered_settings_plugins[node_type])
                    print(node_type)
                instance.generic_visit(node)
            setattr(self, "visit_" + node_type, types.MethodType(func, self))

    def __init__(self, file):
        super().__init__(file)
        self.create_visitor_functions()
