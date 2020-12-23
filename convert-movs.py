#!/usr/bin/env python3
from mediawalker import MediaFileWalker
import os
import sys


def convertVideoFile(fileName):
    basePath, extension = os.path.splitext(fileName)
    if extension.lower() != '.mov':
        return
    print(f'Converting {fileName} to mp4...')
    mp4Path = basePath + '.mp4'
    if os.path.exists(mp4Path):
        print(f'  {mp4Path} already exists, skipping')
        return
    os.system(f'ffmpeg -hide_banner -loglevel fatal -i {fileName} -q:v 0 {mp4Path}')


def main(args):
    if len(args) != 1:
        print('You must specify just a path the the media root')
        return -1
    
    walker = MediaFileWalker()
    walker.walk(args[0], convertVideoFile)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))