import argparse  # recommended command-line parsing module for python
import os


def parse_args(args):
    if len(args) == 0:
        args.append('-h')  # if no arguments are given, print usage

    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="directory to guard")  # required argument
    parser.add_argument("-r", "--recursive", action='store_true',
                        help="guard all source files in subdirectories")  # optional argument
    parser.add_argument("-w", "--watchdog", action='store_true',
                        help="after initial scan enter watchdog mode where saving a .py file triggers a new scan of "
                             "that file")  # optional argument
    parser.add_argument("-x", "--exclude", nargs="+",
                        help="exclude directories from vulnerability scan")  # optional argument
    args = parser.parse_args(args)

    if args.target is None:
        parser.error('The target argument is required')
    if args.exclude:
        args.exclude[:] = [os.path.normpath(os.path.join(args.target, x)) for x in args.exclude]
    return args
