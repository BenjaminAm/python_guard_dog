import os
from ast_helper.ast_builder import build_ast
from analyzer.analyzer import Analyzer


def scan_file(path):
    path = os.path.normpath(path)
    tree = build_ast(path)
    analyzer = Analyzer(path)
    analyzer.visit(tree)
    analyzer.report()


def find_py_files(dir_path, recursive, exclude):
    found_files = []
    if recursive:
        for root, dirs, files in os.walk(dir_path, topdown=True):
            if exclude and isinstance(exclude, list):
                dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in exclude]

            for file in files:
                if file.endswith(".py"):  # only python source code will be scanned.
                    found_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(dir_path):
            if file.endswith(".py"):
                found_files.append(os.path.join(dir_path, file))
    return found_files
