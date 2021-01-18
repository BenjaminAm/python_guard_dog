import os
from watchdog.events import PatternMatchingEventHandler, FileModifiedEvent
from scan import scan_file


def on_modified(event):
    if not isinstance(event, FileModifiedEvent):
        return
    if event.src_path[-3:] == ".py":
        scan_file(event.src_path)


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
    event_handler.on_modified = on_modified
    event_handler.on_deleted = on_deleted
    event_handler.on_moved = on_moved
    return event_handler
