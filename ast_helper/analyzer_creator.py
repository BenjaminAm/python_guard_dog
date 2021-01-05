from .analyzer import Analyzer
from .settings_analyzer import SettingsAnalyzer


def create_analyzer(file):
    if file.endswith("settings.py"):
        return SettingsAnalyzer(file)
    else:
        return Analyzer(file)