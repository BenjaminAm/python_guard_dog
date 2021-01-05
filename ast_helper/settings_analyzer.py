from .analyzer import Analyzer
from .vulnerability import Vulnerability


class SettingsAnalyzer(Analyzer):
    def __init__(self, file):
        super().__init__(file)

    django_security_found = django_csrf_found = False

    def visit_Assign(self, node):
        for target in node.targets:
            if target.id == "DEBUG":
                if node.value.value == True:
                    self.vulnerabilities.append(Vulnerability(file=self.file, lineno=node.lineno,
                                                              vuln_type=Vulnerability.djdebug))
            if target.id == "MIDDLEWARE":
                for constant in node.value.elts:
                    if constant.value == "django.middleware.security.SecurityMiddleware":
                        self.django_security_found = True
                    if constant.value == "django.middleware.csrf.CsrfViewMiddleware":
                        self.django_csrf_found = True
        self.generic_visit(node)

    def visit_Module(self, node):
        self.generic_visit(node)
        if not self.django_security_found:
            self.vulnerabilities.append(Vulnerability(file=self.file, vuln_type=Vulnerability.djsecmidw))
        if not self.django_security_found:
            self.vulnerabilities.append(Vulnerability(file=self.file, vuln_type=Vulnerability.djcsrfmidw))