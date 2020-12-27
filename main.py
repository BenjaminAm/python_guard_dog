import time
import os
from watchdog.observers import Observer
from usage import parse_args
import sys
from event_handler import build_event_handler


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    path = os.path.normpath(args.filepath)

    event_handler = build_event_handler()
    my_observer = Observer()
    my_observer.schedule(event_handler, args.target, recursive=args.recursive)
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
