#!/usr/bin/env python3
from mediaclient import MediaClient
from photomanager import PhotoManager
import sys


def replicateAlbum(source, destination):
    errors = []
    manager = PhotoManager(source)
    client = MediaClient(destination)
    for folderName in manager.folders:
        print(f'Replicating folder {folderName}...')
        if not client.folderExists(folderName):
            if client.createFolder(folderName):
                print(f'  Successfully created folder {folderName}')
            else:
                error = f'  Failed to create folder {folderName}. Not uploading folder images'
                errors.append(error)
                print(error)
                continue
        else:
            print('  Folder {folderName} already exists')
        folder = manager.folder(folderName)
        for imageName in folder.images:
            print(f'  Replicating image {imageName}...')
            if not client.imageExists(folderName, imageName):
                print(f'    Uploading image {imageName}...')
                image = folder.image(imageName)
                if client.uploadImage(folderName, imageName, image.content):
                    print(f'    Successfully uploading image {imageName}')
                else:
                    error = f'    Failed to upload image {imageName}'
                    errors.append(error)
                    print(error)
            else:
                print(f'    Image {imageName} already exists')
            print(f'  Done replicating image {imageName}')
        print(f'Done replicating folder {folderName}')
    print(f'\nReplication completed with {len(errors)} errors')
    if len(errors) > 0:
        print('Errors:')
        for error in errors:
            print(f'  {error}')

def main(args):
    if len(args) < 2:
        print('Not enought arguments. expect source folder and destination server')
        sys.exit(-1)
    if len(args) > 2:
        print('Too many arguments. expect source folder and destination server')
        sys.exit(-1)
    source, destination = args
    replicateAlbum(source, destination)


if __name__ == "__main__":
    main(sys.argv[1:])