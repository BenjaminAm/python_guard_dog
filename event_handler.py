import os
from watchdog.events import PatternMatchingEventHandler, FileModifiedEvent
from ast_helper.ast_builder import build_ast
from ast_helper.analyzer_creator import create_analyzer


def scan_file(event):
    if not isinstance(event, FileModifiedEvent):
        return
    path = os.path.normpath(event.src_path)
    if path[-1] == "~":  # temporary IDE files will not be scanned
        return
    if path[-3:] == ".py":  # only python source code will be scanned.
        tree = build_ast(path)
        analyzer = create_analyzer(path)
        analyzer.visit(tree)
        report = analyzer.report()
        for vulnerability in report:
            print(vulnerability)
        print("----------------------")


def on_created(event):
    pass


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
    event_handler.on_created = on_created
    event_handler.on_modified = scan_file
    event_handler.on_deleted = on_deleted
    event_handler.on_moved = on_moved
    return event_handler
