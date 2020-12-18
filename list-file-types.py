#!/usr/bin/env python3
import os
import sys


def listFolders(path):
    return [os.path.join(path, child) for child in os.listdir(path) if os.path.isdir(os.path.join(path, child))]

def listFiles(path):
    return [os.path.join(path, child) for child in os.listdir(path) if os.path.isfile(os.path.join(path, child))]

def main(args):
    extensions = set()
    if len(args) != 1:
        print('Unexpected command line. Expect folder path')
        sys.exit(-1)
    for folder in listFolders(args[0]):
        for file in listFiles(folder):
            path, ext = os.path.splitext(file)
            if len(ext) == 0:
                continue
            ext = ext[1:]
            extensions.add(ext)
    print(extensions)

if __name__ == "__main__":
    main(sys.argv[1:])