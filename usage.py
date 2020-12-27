import argparse  # recommended command-line parsing module for python


def parse_args(args):
    if len(args) == 0:
        args.append('-h')  # if no arguments are given, print usage

    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="directory to guard")  # required argument
    parser.add_argument("-r", "--recursive", action='store_true',
                        help="guard all source files in subdirectories")  # optional argument
    args = parser.parse_args(args)

    if args.target is None:
        parser.error('The target argument is required')
    return args
