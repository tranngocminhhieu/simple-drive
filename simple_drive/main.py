import os
import os.path

from colorama import Fore
from googleapiclient.discovery import build
from pydrive2.drive import GoogleDrive


class Drive:
    def __init__(self, auth_info, verbose=True):
        '''
        Use Google Drive API in the simplest way
        :param auth_info: Use Auth class to authenticate with Google Drive
        :param verbose: Print result
        '''
        self.verbose = verbose

        # For Upload and List files
        self.drive = GoogleDrive(auth_info)

        # For other features
        self.service = build('drive', 'v3', credentials=auth_info.credentials)

        # Default info result of service.files()
        self.default_file_fields = 'id, name, mimeType, parents, webViewLink, owners'

    # Support
    def print_if_vebose(self, *args):
        if self.verbose:
            print(*args)

    # File interaction
    def create(self, name, mime_type, dest_folder_id=None):
        '''
        Create a file|folder
        :param name: File|folder name
        :param mime_type: Use constants.MimeTypes or visit https://developers.google.com/drive/api/guides/mime-types
        :param dest_folder_id: Destination folder
        :return: File|folder info
        '''
        body = {
            'name': name,
            'mimeType': mime_type,
        }
        if dest_folder_id:
            body['parents'] = [dest_folder_id]

        file = self.service.files().create(body=body, fields=self.default_file_fields).execute()

        self.print_if_vebose(f"{Fore.GREEN}Created {Fore.RESET}{name}")

        return file

    def delete(self, file_id):
        '''
        Delete a file|folder
        :param file_id: File|folder ID
        '''
        self.service.files().delete(fileId=file_id).execute()
        self.print_if_vebose(f"{Fore.RED}Deleted file|folder {Fore.RESET}{file_id}")

    def move(self, file_id, dest_folder_id):
        '''
        Move a file|folder
        :param file_id: File|folder ID
        :param dest_folder_id: Destination folder
        :return: File|folder info
        '''
        file = self.service.files().get(fileId=file_id, fields=self.default_file_fields).execute()
        remove_parents = file['parents'][0]
        result = self.service.files().update(fileId=file_id,
                                             addParents=dest_folder_id,
                                             removeParents=remove_parents,
                                             fields=self.default_file_fields).execute()

        self.print_if_vebose(f"{Fore.BLUE}Moved file|folder {Fore.RESET}{file_id}{Fore.BLUE} to folder {Fore.RESET}{dest_folder_id}")

        return result

    def upload(self, file, dest_folder_id=None, rename=None):
        '''
        Upload a file
        :param file: Local file
        :param dest_folder_id: Destination folder
        :param rename: Rename file before uploading
        :return: File info
        '''
        title = rename if rename else os.path.split(file)[-1]  # Avoid local dir in name
        parents = [{'id': dest_folder_id}] if dest_folder_id else None

        metadata = {
            'title': title,
            'parents': parents
        }

        new_file = self.drive.CreateFile(metadata=metadata)
        new_file.SetContentFile(file)
        new_file.Upload()

        self.print_if_vebose(f"{Fore.GREEN}Uploaded file {Fore.RESET}{title}{f'{Fore.GREEN} to folder {Fore.RESET}{dest_folder_id}' if dest_folder_id else ''}")

        return new_file

    def get_file_info(self, file_id, fields='*'):
        '''
        Get a file|folder info
        :param file_id: File|folder ID
        :param fields: * is all fields
        :return: File|folder info
        '''
        return self.service.files().get(fileId=file_id, fields=fields).execute()

    def copy(self, file_id, name_prefix='Copy of ', name_suffix='', dest_folder_id=None):
        '''
        Copy a file. Not support folder yet.
        :param file_id: File ID
        :param name_prefix: Default to 'Copy of '
        :param name_suffix: Default to ''
        :param dest_folder_id: Destination folder
        :return: File info
        '''
        current_file = self.service.files().get(fileId=file_id, fields=self.default_file_fields).execute()
        current_name = current_file['name']
        new_name = f'{name_prefix}{current_name}{name_suffix}'

        body = {'name': new_name}
        if dest_folder_id:
            body['parents'] = [dest_folder_id]

        new_file = self.service.files().copy(fileId=file_id, body=body, fields=self.default_file_fields).execute()

        self.print_if_vebose(f"{Fore.GREEN}Copied {Fore.RESET}{current_name}{Fore.GREEN} to {Fore.RESET}{new_name}")

        return new_file

    def rename(self, file_id, name):
        '''
        Rename a file|folder
        :param file_id: File|folder ID
        :param name: Renamed name
        :return: File|folder info
        '''
        body = {'name': name}
        result = self.service.files().update(fileId=file_id, body=body, fields=self.default_file_fields).execute()
        self.print_if_vebose(f"{Fore.BLUE}Renamed file|folder {Fore.RESET}{file_id} {Fore.BLUE}to {Fore.RESET}{name}")
        return result

    # Account infomation
    def list_files(self, title_contains=None, owner_email=None, folder_id=None, custom_filter=None):
        '''
        List files related to this account
        :param title_contains: Filter by title
        :param owner_email: Filter by owner
        :param folder_id: Filter by folder
        :param custom_filter: Your custom filter
        :return: List of files
        '''
        filters = []
        if title_contains:
            filters.append(f"title contains '{title_contains}'")
        if owner_email:
            filters.append(f"'{owner_email}' in owners")
        if folder_id:
            filters.append(f"'{folder_id}' in parents and trashed=false")
        if custom_filter:
            filters.append(custom_filter)

        param = {'q': ' and '.join(filters)} if len(filters) else None

        files = self.drive.ListFile(param=param).GetList()

        return files

    def storage_quota(self):
        '''
        Get the account storage quota
        :return: Storage quota info
        '''
        about = self.service.about().get(fields="*").execute()
        quota = about.get("storageQuota", {})
        return quota

    # Permission
    def add_permission(self, file_id, email, role):
        '''
        Add permission to a file|folder
        :param file_id: File|folder ID
        :param email: Email address
        :param role: Use constants.Roles or visit https://developers.google.com/drive/api/guides/ref-roles
        :return: Permission info
        '''
        body = {'type': 'user', 'role': role, 'emailAddress': email}
        result = self.service.permissions().create(fileId=file_id, body=body, fields='*').execute()
        self.print_if_vebose(
            f"{Fore.GREEN}Added {Fore.RESET}{role} {Fore.GREEN}permission for {Fore.RESET}{email} {Fore.GREEN}to {Fore.RESET}{file_id}")
        return result

    def get_permission_info(self, file_id):
        '''
        Get permission of a file|folder
        :param file_id: File|folder ID
        :return: Permission info
        '''
        return self.service.permissions().list(fileId=file_id, fields='permissions').execute()['permissions']

    def remove_permission(self, file_id, email=None, permission_id=None):
        '''
        Remove a permission from a file|folder
        :param file_id: File|folder ID
        :param email: Email address
        :param permission_id: Permission ID
        '''
        if permission_id:
            pass
        elif email:
            permissions = self.get_permission_info(file_id=file_id)
            permission = [p['id'] for p in permissions if p['emailAddress'] == email]
            if not permission:
                raise ValueError(f"{email} does not exist in permission list")
            else:
                permission_id = permission[0]
        else:
            raise ValueError(f"Please provide either email or permission_id")

        self.service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()

        self.print_if_vebose(f"{Fore.RED}Removed permission of {Fore.RESET}{email or permission_id} {Fore.RED}from {Fore.RESET}{file_id}")

    def transfer_ownership(self, file_id, email):
        '''
        Transfer ownership of a file|folder to an email
        :param file_id: File|folder ID
        :param email: Email address
        :return: Ownership info
        '''
        body = {'type': 'user', 'role': 'owner', 'emailAddress': email}
        result = self.service.permissions().create(fileId=file_id, body=body, transferOwnership=True,
                                                   fields='*').execute()
        self.print_if_vebose(f"{Fore.BLUE}Transferred ownership of {Fore.RESET}{file_id} {Fore.BLUE}to {Fore.RESET}{email}")
        return result