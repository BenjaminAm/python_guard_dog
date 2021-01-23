import time, os, sys
from watchdog.observers import Observer
from usage import parse_args
from event_handler import build_event_handler
from scan import find_py_files, scan_file
from importlib import import_module


def register_plugins():
    for file in os.listdir(os.path.normpath("vulnerability/plugins/")):
        if file.endswith(".py"):
            module = "vulnerability.plugins." + file[:-3]
            import_module(module)  # import plugins so that they are registered by their decorators


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])

    register_plugins()

    # run scan once on all source files in directory
    py_files = find_py_files(args.target, args.recursive, args.exclude)
    for py_file in py_files:
        scan_file(py_file)

    if args.watchdog:
        event_handler = build_event_handler()

        observer = Observer()
        observer.schedule(event_handler, args.target, recursive=args.recursive)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
