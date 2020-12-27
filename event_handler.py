import os
from watchdog.events import PatternMatchingEventHandler
from .ast.ast_builder import build_ast, Analyzer


def scan_file(event):
    path = os.path.normpath(event.src_path)
    tree = build_ast(event.src_path)

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()

def on_deleted(event):
    pass


def on_moved(event):
    pass


def build_event_handler():
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = True
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    event_handler.on_created = scan_file
    event_handler.on_modified = scan_file
    event_handler.on_deleted = on_deleted
    event_handler.on_moved = on_moved
    return event_handler
