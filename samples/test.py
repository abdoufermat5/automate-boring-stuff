import os

from drive_me.MyDrive import MyDrive
from drive_me.utils.helpers import create_random_structure, publish_to_drive

if __name__ == '__main__':
    # create root folder
    root_folder = os.path.join(os.getcwd(), 'root_folder')
    # create folder if it does not exist
    if not os.path.exists(root_folder):
        os.mkdir(root_folder)
    # create random structure
    create_random_structure(root_folder, 5, 5, 2)
    # publish to drive
    my_drive = MyDrive()
    f_title = "MY-AUTOMATED-FOLDER"
    f_id = ""
    if not my_drive.get_folder_id(f_title):
        f_id = my_drive.create_folder(f_title)
    else:
        f_id = my_drive.get_folder_id(f_title)

    publish_to_drive(my_drive, root_folder, f_title)
