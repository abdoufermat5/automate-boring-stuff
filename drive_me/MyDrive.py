import os
from treelib import Node, Tree
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


class MyDrive:
    def __init__(self):
        """
        This class is used to work with Google Drive
        """
        self.gAuth = GoogleAuth()
        current_path = os.path.dirname(os.path.abspath(__file__))
        # check if folder contains secrets.txt file
        if os.path.isfile(os.path.join("../data", "my_secrets.txt")):
            self.gAuth.LoadCredentialsFile(os.path.join("../data", "my_secrets.txt"))
        self.gAuth.LocalWebserverAuth()
        # save credentials to file
        if not os.path.isfile(os.path.join("../data", "my_secrets.txt")):
            self.gAuth.SaveCredentialsFile(os.path.join(current_path, "../data/my_secrets.txt"))
        self.drive = GoogleDrive(self.gAuth)

    def create_folder(self, folder_name):
        """
        This method is used to create a folder on Google Drive
        :param folder_name: name of the folder to be created
        :return: folder_id
        """
        folder = self.drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
        folder.Upload()
        print(f"Folder {folder_name} created successfully")
        return folder['id']

    def create_folder_in(self, folder_name, parent_folder_id):
        """
        This method is used to create a folder in a specific folder on Google Drive
        :param folder_name: name of the folder to be created
        :param parent_folder_id: id of the parent folder
        :return: folder_id
        """
        folder = self.drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder',
                                        'parents': [{'id': parent_folder_id}]})
        folder.Upload()
        print(f"Folder {folder_name} created successfully")
        return folder['id']

    def get_folder_id(self, folder_name):
        """
        This method is used to get the id of a folder on Google Drive
        :param folder_name: name of the folder
        :return: folder_id
        """
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == folder_name:
                return file['id']
        return False

    def check_if_folder_in(self, folder_id, folder_name):
        """
        This method is used to check if a folder exists in a specific folder on Google Drive
        :param folder_id: id of the folder
        :param folder_name: name of the folder
        :return: folder_id
        """
        file_list = self.get_folder_children(folder_id)
        for file in file_list:
            if file['title'] == folder_name:
                return file['id']
        return False

    def check_if_file_in(self, folder_id, file_name):
        """
        This method is used to check if a file exists in a specific folder on Google Drive
        :param folder_id: id of the folder
        :param file_name: name of the file
        :return: file_id
        """
        file_list = self.get_folder_children(folder_id)
        for file in file_list:
            if file['title'] == file_name:
                return file['id']
        return False

    def get_folder_children(self, folder_id):
        """
        This method is used to get the children of a folder on Google Drive
        :param folder_id: id of the folder
        :return: list of children
        """
        file_list = self.drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
        return file_list

    def send_folder(self, _path, folder_name):
        """
        This method is used to upload a folder to Google Drive
        :param _path: folder path in local machine
        :param folder_name: name of the folder to be uploaded
        :return: None
        """
        folder_id = self.create_folder(folder_name)
        for file in os.listdir(_path):
            file_drive = self.drive.CreateFile({'title': file, 'parents': [{'id': folder_id}]})
            file_drive.SetContentFile(os.path.join(_path, file))
            file_drive.Upload()

        print("Folder uploaded successfully")

    def upload_file(self, filename, folder_id, from_path):
        """
        This method is used to upload a file to Google Drive
        :param filename: name of the file to be uploaded
        :param folder_id: id of the folder
        :param from_path: path of the file in local machine
        :return: None
        """
        file_drive = self.drive.CreateFile({'title': filename, 'parents': [{'id': folder_id}]})
        file_drive.SetContentFile(from_path)
        file_drive.Upload()
        print("File uploaded successfully")

    def upload_to_root(self, _path, file_name):
        """
        This method is used to upload a file to Google Drive
        :param _path: file path in local machine
        :param file_name: name of the file to be uploaded
        :return: None
        """
        file_drive = self.drive.CreateFile({'title': file_name})
        file_drive.SetContentFile(os.path.join(_path, file_name))
        file_drive.Upload()
        print("File uploaded successfully")

    def get_file_and_save_to(self, file_id, _path):
        """
        This method is used to download a file from Google Drive
        :param file_id: id of the file
        :param _path: path to save the file
        :return: None
        """
        file_drive = self.drive.CreateFile({'id': file_id})
        file_drive.GetContentFile(os.path.join(_path, file_drive['title']))
        print("File downloaded successfully")

    def get_folder_and_save_to(self, folder_id, _path):
        """
        This method is used to download a folder from Google Drive
        :param folder_id: id of the folder
        :param _path: path to save the folder
        :return: None
        """
        tree = Tree()
        root = tree.create_node("root", folder_id)
        self.add_children_to_tree(folder_id, tree, root)
        for node in tree.expand_tree(mode=tree.WIDTH):
            if node.is_leaf():
                file_drive = self.drive.CreateFile({'id': node, 'parents': [{'id': folder_id}]})
                file_drive.GetContentFile(os.path.join(_path, file_drive['title']))
        print("Folder downloaded successfully")

    def move_file(self, file_id, from_folder_id, to_folder_id):
        """
        This method is used to move a file from one folder to another
        :param file_id: id of the file
        :param from_folder_id: id of the folder to move from
        :param to_folder_id: id of the folder to move to
        :return: None
        """
        file_drive = self.drive.CreateFile({'id': file_id})
        file_drive['parents'] = [{'id': to_folder_id}]
        file_drive.Upload()
        print("File moved successfully")
        # delete file from old folder
        self.delete_file_from_folder(file_id, from_folder_id)
        print("File deleted from old folder successfully")

    def move_folder(self, folder_id, from_folder_id, to_folder_id):
        """
        This method is used to move a folder from one folder to another
        :param folder_id: id of the folder
        :param from_folder_id: id of the folder to move from
        :param to_folder_id: id of the folder to move to
        :return: None
        """
        folder_drive = self.drive.CreateFile({'id': folder_id})
        folder_drive['parents'] = [{'id': to_folder_id}]
        folder_drive.Upload()
        print("Folder moved successfully")
        # delete folder from old folder
        self.delete_folder_from_folder(folder_id, from_folder_id)
        print("Folder deleted from old folder successfully")

    def search_file_in_all_folders(self, file_name):
        """
        This method is used to search for a file in all folders on Google Drive
        :param file_name: name of the file
        :return: file_id
        """
        file_list = self.drive.ListFile({'q': "trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == file_name:
                return file['id']
        return False

    def search_folder_in_all_folders(self, folder_name):
        """
        This method is used to search for a folder in all folders on Google Drive
        :param folder_name: name of the folder
        :return: folder_id
        """
        file_list = self.drive.ListFile({'q': "trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == folder_name:
                return file['id']
        return False

    def delete_file(self, file_id):
        """
        This method is used to delete a file from Google Drive
        :param file_id: id of the file
        :return: None
        """
        file_drive = self.drive.CreateFile({'id': file_id})
        file_drive.Trash()
        print("File deleted successfully")

    def delete_file_from_folder(self, file_id, folder_id):
        """
        This method is used to delete a file from a specific folder on Google Drive
        :param file_id: id of the file
        :param folder_id: id of the folder
        :return: None
        """
        file_drive = self.drive.CreateFile({'id': file_id})
        file_drive['parents'] = [{'id': folder_id}]
        file_drive.Trash()

    def delete_folder(self, folder_id):
        """
        This method is used to delete a folder from Google Drive
        :param folder_id: id of the folder
        :return: None
        """
        tree = Tree()
        root = tree.create_node("root", folder_id)
        self.add_children_to_tree(folder_id, tree, root)
        for node in tree.expand_tree(mode=tree.WIDTH):
            file_drive = self.drive.CreateFile({'id': node, 'parents': [{'id': folder_id}]})
            file_drive.Trash()
        print("Folder deleted successfully")

    def delete_folder_from_folder(self, folder_id, parent_folder_id):
        """
        This method is used to delete a folder from a specific folder on Google Drive
        :param folder_id: id of the folder
        :param parent_folder_id: id of the parent folder
        :return: None
        """
        tree = Tree()
        root = tree.create_node("root", folder_id)
        self.add_children_to_tree(folder_id, tree, root)
        for node in tree.expand_tree(mode=tree.WIDTH):
            file_drive = self.drive.CreateFile({'id': node, 'parents': [{'id': folder_id}]})
            file_drive['parents'] = [{'id': parent_folder_id}]
            file_drive.Trash()
        print("Folder deleted successfully")

    def restore_file(self, file_id):
        """
        This method is used to restore a file from Google Drive
        :param file_id: id of the file
        :return: None
        """
        file_drive = self.drive.CreateFile({'id': file_id})
        file_drive.UnTrash()
        print("File restored successfully")

    def restore_folder(self, folder_id):
        """
        This method is used to restore a folder from Google Drive
        :param folder_id: id of the folder
        :return: None
        """
        tree = Tree()
        root = tree.create_node("root", folder_id)
        self.add_children_to_tree(folder_id, tree, root)
        for node in tree.expand_tree(mode=tree.WIDTH):
            file_drive = self.drive.CreateFile({'id': node, 'parents': [{'id': folder_id}]})
            file_drive.UnTrash()
        print("Folder restored successfully")

    def add_children_to_tree(self, folder_id, tree, parent_node):
        """
        This method is used to add children to a tree object
        :param folder_id: id of the folder
        :param tree: tree object
        :param parent_node: parent node
        :return: None
        """
        file_list = self.get_folder_children(folder_id)
        for file in file_list:
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                node = tree.create_node(file['title'], file['id'], parent=parent_node)
                self.add_children_to_tree(file['id'], tree, node)
            else:
                tree.create_node(file['title'], file['id'], parent=parent_node)
