import os
import random
import string
import json


# create a tree structure with random files and folders in current directory and publish to google drive
def create_random_files(folder_path, number_of_files):
    """
    This method is used to create random files in a folder
    :param folder_path: path of the folder
    :param number_of_files: number of files to be created
    :return: None
    """
    for i in range(number_of_files):
        file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        with open(os.path.join(folder_path, file_name), 'w') as f:
            f.write("This is a random file")
            print(f"File {file_name} created successfully")


def create_random_folders(folder_path, number_of_folders):
    """
    This method is used to create random folders in a folder
    :param folder_path: path of the folder
    :param number_of_folders: number of folders to be created
    :return: None
    """
    for i in range(number_of_folders):
        folder_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        os.mkdir(os.path.join(folder_path, folder_name))
        print(f"Folder {folder_name} created successfully")


def create_random_structure(folder_path, number_of_files, number_of_folders, depth):
    """
    This method is used to create a random structure of files and folders in a folder
    :param folder_path: path of the folder
    :param number_of_files: number of files to be created
    :param number_of_folders: number of folders to be created
    :param depth: depth of the tree
    :return: None
    """
    create_random_files(folder_path, number_of_files)
    create_random_folders(folder_path, number_of_folders)
    if depth > 0:
        for folder in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, folder)):
                create_random_structure(os.path.join(folder_path, folder), number_of_files, number_of_folders,
                                        depth - 1)


# publish the tree structure to google drive by creating folders and uploading files from the tree structure
def publish_to_drive(drive, root_folder, drive_folder_name):
    """
    This method is used to publish a tree structure to google drive
    :param drive: instance of MyDrive class
    :param root_folder: root folder of the tree structure
    :param drive_folder_name: name of the folder to be created in google drive
    :return: None
    """
    # create a dictionary to store the folder structure
    folder_structure = {}
    # create a folder in google drive if it does not exist
    if not drive.get_folder_id(drive_folder_name):
        drive_folder_id = drive.create_folder(drive_folder_name)
    else:
        drive_folder_id = drive.get_folder_id(drive_folder_name)
    # add the drive_folder_id to the dictionary
    folder_structure[drive_folder_name] = drive_folder_id
    # iterate through the root folder
    for folder in os.listdir(root_folder):
        # if the folder is a directory
        if os.path.isdir(os.path.join(root_folder, folder)):
            # create the directory in google drive
            drive_folder_id = drive.create_folder_in(folder, parent_folder_id=drive_folder_id)
            # add the folder to the dictionary
            folder_structure[folder] = drive_folder_id
            # iterate through the files in the folder
            for file in os.listdir(os.path.join(root_folder, folder)):
                # if the file is a file
                if os.path.isfile(os.path.join(root_folder, folder, file)):
                    # upload the file to google drive
                    drive.upload_file(file, folder_id=drive_folder_id,
                                      from_path=os.path.join(root_folder, folder, file))
                    print(f"File {file} uploaded to google drive")
            # iterate through the sub folders
            for sub_folder in os.listdir(os.path.join(root_folder, folder)):
                # if the sub folder is a directory
                if os.path.isdir(os.path.join(root_folder, folder, sub_folder)):
                    # create the sub folder in google drive
                    drive_folder_id = drive.create_folder_in(sub_folder, parent_folder_id=folder_structure[folder])
                    # add the sub folder to the dictionary
                    folder_structure[sub_folder] = drive_folder_id
                    # iterate through the files in the sub folder
                    for file in os.listdir(os.path.join(root_folder, folder, sub_folder)):
                        # if the file is a file
                        if os.path.isfile(os.path.join(root_folder, folder, sub_folder, file)):
                            # upload the file to google drive
                            drive.upload_file(file, folder_id=drive_folder_id,
                                              from_path=os.path.join(root_folder, folder, sub_folder, file))
                            print(f"File {file} uploaded to google drive")


def write_json(data, to_path, filename):
    """
    This method is used to write a json file
    :param data: data to be written
    :param to_path: path to write the file
    :param filename: name of the file
    :return: None
    """
    with open(os.path.join(to_path, filename), 'w') as f:
        json.dump(data, f, indent=4)
        print(f"File {filename} written successfully")


def read_json(from_path, filename):
    """
    This method is used to read a json file
    :param from_path: path to read the file
    :param filename: name of the file
    :return: data
    """
    with open(os.path.join(from_path, filename), 'r') as f:
        data = json.load(f)
        print(f"File {filename} read successfully")
        return data
