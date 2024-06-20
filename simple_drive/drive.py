import os
import os.path
from enum import Enum

from colorama import Fore
from googleapiclient.discovery import build
from pydrive2.drive import GoogleDrive
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io

from .constants import MimeTypes


class Drive:
    def __init__(self, auth, verbose=True):
        '''
        Use Google Drive API in the simplest way
        :param auth_info: Use Auth class to authenticate with Google Drive
        :param verbose: Print result
        '''
        self.verbose = verbose

        # For Upload and List files
        self.google_drive = GoogleDrive(auth)

        # For other features
        self.service = build('drive', 'v3', credentials=auth.credentials)

        self.Files = self.Files(drive=self)
        self.Comments = self.Comments(drive=self)
        self.Permissions = self.Permissions(drive=self)
        self.Replies = self.Replies(drive=self)
        self.Revisions = self.Revisions(drive=self)

    # Support
    def print_if_verbose(self, *args):
        if self.verbose:
            print(*args)


    def get_storage_quota(self):
        '''
        Get the account storage quota
        :return: Storage quota info
        '''
        quota = self.service.about().get(fields="storageQuota").execute()['storageQuota']
        try:
            limit = round(int(quota['limit']) / 1024 / 1024 / 1024, 2)
            usage = round(int(quota['usage']) / 1024 / 1024 / 1024, 2)
            usage_percent = round(usage / limit * 100, 2)
            if usage_percent < 30:
                color = Fore.GREEN
            elif usage_percent < 70:
                color = Fore.YELLOW
            else:
                color = Fore.RED
            self.print_if_verbose(f"{color}{usage:0,.2f} GB{Fore.RESET} / {limit:0,.2f} GB (usage {usage_percent}%)")
        except:
            pass

        return quota

    def get_about(self):
        return self.service.about().get(fields="*").execute()

    class Files:
        def __init__(self, drive):
            self.drive = drive
            self.default_file_fields = 'id, name, mimeType, parents, webViewLink, owners'

        # File interaction
        def create(self, name, mime_type, dest_folder_id=None):
            '''
            Create a file|folder
            :param name: File|folder name
            :param mime_type: Use constants.MimeTypes or visit https://developers.google.com/drive/api/guides/mime-types
            :param dest_folder_id: Destination folder
            :return: File|folder info
            '''

            if isinstance(mime_type, Enum):
                mime_type_value = mime_type.value
                mime_type_name = mime_type.name.capitalize()
            else:
                mime_type_value = mime_type.lower()
                mime_type_name = mime_type.capitalize()

            if mime_type_value == MimeTypes.SHORTCUT.value:
                raise Exception('Please use create_shortcut instead')

            body = {
                'name': name,
                'mimeType': mime_type_value,
            }
            if dest_folder_id:
                body['parents'] = [dest_folder_id]

            file = self.drive.service.files().create(body=body, fields=self.default_file_fields).execute()

            self.drive.print_if_verbose(f"{Fore.GREEN}Created {'an' if mime_type_name[0].lower() in 'ueoai' else 'a'} {mime_type_name} as {Fore.RESET}{name}{f'{Fore.GREEN} in folder {Fore.RESET}{dest_folder_id}' if dest_folder_id else ''}")

            return file

        def create_shortcut(self, file_id, name=None, dest_folder_id=None):
            '''
            Create a shortcut
            :param file_id: File ID
            :param shortcut_name: Shortcut name
            :param dest_folder_id: Destination folder
            :return: Shortcut info
            '''
            if not name:
                name = self.get_file_info(file_id=file_id).get('name')

            shortcut_metadata = {
                'Name': name,
                'mimeType': MimeTypes.SHORTCUT.value,
                'shortcutDetails': {
                    'targetId': file_id
                }
            }

            if dest_folder_id:
                shortcut_metadata['parents'] = [dest_folder_id]

            shortcut = self.drive.service.files().create(body=shortcut_metadata, fields=f'{self.default_file_fields},shortcutDetails').execute()

            self.drive.print_if_verbose(f"{Fore.GREEN}Created a shortcut of {Fore.RESET}{file_id}{Fore.GREEN} as {Fore.RESET}{name}")
            return shortcut

        def delete(self, file_id):
            '''
            Delete a file|folder
            :param file_id: File|folder ID
            '''
            self.drive.service.files().delete(fileId=file_id).execute()
            self.drive.print_if_verbose(f"{Fore.RED}Deleted {Fore.RESET}{file_id}")


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

            new_file = self.drive.google_drive.CreateFile(metadata=metadata)
            new_file.SetContentFile(file)
            new_file.Upload()

            self.drive.print_if_verbose(f"{Fore.GREEN}Uploaded {Fore.RESET}{title}{f'{Fore.GREEN} to folder {Fore.RESET}{dest_folder_id}' if dest_folder_id else ''}")

            return new_file


        def move(self, file_id, dest_folder_id):
            '''
            Move a file|folder
            :param file_id: File|folder ID
            :param dest_folder_id: Destination folder
            :return: File|folder info
            '''
            file = self.drive.service.files().get(fileId=file_id, fields=self.default_file_fields).execute()
            remove_parents = file['parents'][0]
            result = self.drive.service.files().update(fileId=file_id,
                                                       addParents=dest_folder_id,
                                                       removeParents=remove_parents,
                                                       fields=self.default_file_fields).execute()

            self.drive.print_if_verbose(f"{Fore.BLUE}Moved {Fore.RESET}{result.get('name', file_id)}{Fore.BLUE} to folder {Fore.RESET}{dest_folder_id}")

            return result


        def copy(self, file_id, name_prefix='Copy of ', name_suffix=None, dest_folder_id=None):
            '''
            Copy a file. Not support folder yet.
            :param file_id: File ID
            :param name_prefix: Default to 'Copy of '
            :param name_suffix: Default to ''
            :param dest_folder_id: Destination folder
            :return: File info
            '''
            current_file = self.drive.service.files().get(fileId=file_id, fields=self.default_file_fields).execute()
            current_name = current_file['name']
            new_name = f"{name_prefix if name_prefix else ''}{current_name}{name_suffix if name_suffix else ''}"

            body = {'name': new_name}
            if dest_folder_id:
                body['parents'] = [dest_folder_id]

            new_file = self.drive.service.files().copy(fileId=file_id, body=body,
                                                       fields=self.default_file_fields).execute()

            self.drive.print_if_verbose(f"{Fore.GREEN}Copied {Fore.RESET}{current_name}{Fore.GREEN} to {Fore.RESET}{new_name}{f'{Fore.GREEN}in folder {Fore.RESET}{dest_folder_id}' if dest_folder_id else ''}")

            return new_file

        def rename(self, file_id, name):
            '''
            Rename a file|folder
            :param file_id: File|folder ID
            :param name: Renamed name
            :return: File|folder info
            '''
            body = {'name': name}
            result = self.drive.service.files().update(fileId=file_id, body=body,
                                                       fields=self.default_file_fields).execute()
            self.drive.print_if_verbose(f"{Fore.BLUE}Renamed {Fore.RESET}{file_id} {Fore.BLUE}to {Fore.RESET}{name}")
            return result

        def get(self, file_id, fields='*'):
            '''
            Get a file|folder info
            :param file_id: File|folder ID
            :param fields: * is all fields
            :return: File|folder info
            '''
            return self.drive.service.files().get(fileId=file_id, fields=fields).execute()

        def list(self, *args, operator='and'):
            '''
            List files related to this account
            :param args: Use SearchTerms or visit https://developers.google.com/drive/api/guides/ref-search-terms
            :param operator: and, or
            :return: List of files
            '''

            filters = [*args]
            param = f" {operator} ".join(filters) if len(filters) else None

            # https://developers.google.com/drive/api/guides/search-files#python
            try:
                # create drive api client
                files = []
                page_token = None
                while True:
                    response = (
                        self.drive.service.files()
                        .list(
                            q=param,
                            spaces="drive",
                            fields="nextPageToken, files(*)",
                            pageToken=page_token,
                        )
                        .execute()
                    )
                    for file in response.get("files", []):
                        # Process change
                        self.drive.print_if_verbose(
                            f"Found file: {Fore.BLUE}{file.get('name')}{Fore.RESET}, {file.get('id')}")
                    files.extend(response.get("files", []))
                    page_token = response.get("nextPageToken", None)
                    if page_token is None:
                        break

            except HttpError as error:
                print(f"An error occurred: {error}")
                files = None

            return files

        def download(self, file_id, dest_directory=None, get_value=False):
            '''
            Download a file from the Drive
            :param file_id: File ID
            :param dest_directory: Destination directory
            :param get_value: False to save the file, True to get the file value only
            :return: file value when get_value is True
            '''
            file_info = self.get_file_info(file_id)

            # https://developers.google.com/drive/api/guides/manage-downloads
            try:
                request = self.drive.service.files().get_media(fileId=file_id)
                file = io.BytesIO()
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    self.drive.print_if_verbose(f"Download {int(status.progress() * 100)}.")

                if dest_directory and not get_value:
                    name = os.path.join(dest_directory, file_info.get('name'))
                else:
                    name = file_info.get('name')

                if not get_value:
                    with open(name, 'wb') as f:
                        f.write(file.getvalue())

                self.drive.print_if_verbose(f"{Fore.GREEN}Downloaded {Fore.RESET}{name}")

            except HttpError as error:
                print(f"An error occurred: {error}")
                file = None

            if get_value:
                return file.getvalue()

        def export(self, file_id, format='default', dest_directory=None, get_value=False):
            '''
            Export the Google Workspace documents
            :param file_id: File ID
            :param format: Format of the exported file (xlsx, docx, pdf, pptx, json, csv, ...), defaults to 'default'. Read more: https://developers.google.com/drive/api/guides/ref-export-formats")
            :param dest_directory: Destination directory
            :param get_value: False to save the file, True to get the file value only
            :return: file value when get_value is True
            '''

            # Prepare export mimeType and format (file mimeType is different with export mimeType)
            file_info = self.get_file_info(file_id=file_id)
            export_formats = {file_info['exportLinks'][v].split('=')[-1]: v for v in file_info['exportLinks']}
            file_mime_type = file_info.get('mimeType')

            if format.lower() not in export_formats and format != 'default':
                raise ValueError(
                    f"You can export {file_id} with formats: {'; '.join(export_formats)}, because it is {file_mime_type}. Read more: https://developers.google.com/drive/api/guides/ref-export-formats")

            # https://developers.google.com/drive/api/guides/ref-export-formats
            default_export_mime_types = {
                # Documents
                MimeTypes.DOCS.value: MimeTypes.DOCX,
                # Spreadsheets
                MimeTypes.SHEETS.value: MimeTypes.XLSX,
                # Presentations
                MimeTypes.SLIDES.value: MimeTypes.PPTX,
                # Drawings
                MimeTypes.DRAWINGS.value: MimeTypes.PDF,
                # Apps Script
                MimeTypes.APPS_SCRIPT.value: MimeTypes.JSON
            }

            if format == 'default':
                export_mime_type = default_export_mime_types[file_mime_type].value
                format = default_export_mime_types[file_mime_type].name.lower()
            else:
                export_mime_type = export_formats[format]

            # https://developers.google.com/drive/api/guides/manage-downloads
            try:
                request = self.drive.service.files().export_media(fileId=file_id, mimeType=export_mime_type)
                file = io.BytesIO()
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    self.drive.print_if_verbose(f"Download {int(status.progress() * 100)}.")

                if dest_directory and not get_value:
                    name = os.path.join(dest_directory, f"{file_info.get('name')}.{format.lower()}")
                else:
                    name = f"{file_info.get('name')}.{format.lower()}"

                if not get_value:
                    with open(name, 'wb') as f:
                        f.write(file.getvalue())

                self.drive.print_if_verbose(f"{Fore.GREEN}Exported {Fore.RESET}{name}")

            except HttpError as error:
                print(f"An error occurred: {error}")
                file = None

            if get_value:
                return file.getvalue()

        def empty_trash(self):
            '''
            Empty the trash
            '''
            self.drive.service.files().emptyTrash().execute()
            self.drive.print_if_verbose(f"{Fore.YELLOW}Already empty trash{Fore.RESET}")

        def trash(self, file_id, restore=False):
            '''
            Trash a file or restore a file from trash
            :param file_id: File|Folder ID
            :param restore: True to restore, False to move to trash
            '''
            body = {'trashed': not restore}
            result = self.drive.service.files().update(fileId=file_id, body=body,
                                                       fields=self.default_file_fields).execute()
            if restore:
                self.drive.print_if_verbose(f"{Fore.GREEN}Restored {Fore.RESET}{file_id}{Fore.GREEN} from trash{Fore.RESET}")
            else:
                self.drive.print_if_verbose( f"{Fore.YELLOW}Moved {Fore.RESET}{file_id}{Fore.YELLOW} to trash{Fore.RESET}")
            return result

        def restrict(self, file_id, read_only=False, owner_restricted=False, reason=None):
            '''
            Restrict the content of a file
            :param file_id: File ID
            :param read_only: True or False
            :param owner_restricted: Only the owner of the file can change the restriction status
            :param reason: Optional
            :return:
            '''
            content_restriction = {'readOnly': read_only, 'ownerRestricted': owner_restricted}
            if reason:
                content_restriction['reason'] = reason

            result = self.drive.service.files().update(fileId=file_id,
                                                       body={'contentRestrictions': [content_restriction]},
                                                       fields=f"{self.default_file_fields},contentRestrictions").execute();

            self.drive.print_if_verbose(f"{Fore.BLUE}Updated content restriction for {Fore.RESET}{file_id}")

            return result


    class Permissions:
        def __init__(self, drive):
            self.drive = drive

        def list(self, file_id):
            '''
            Get a list of permissions of a file|folder
            :param file_id: File|folder ID
            :return: Permission info
            '''
            return self.drive.service.permissions().list(fileId=file_id, fields='permissions').execute()['permissions']

        def add(self, file_id, role, email=None, domain=None):
            '''
            Add permission to a file|folder
            :param file_id: File|folder ID
            :param role: Use constants.Roles or visit https://developers.google.com/drive/api/guides/ref-roles
            :param email: Email address
            :param domain: Domain, e.g. google.com
            :return: Permission info
            '''

            provided_args = [email, domain]
            provided_count = sum(arg is not None for arg in provided_args)
            if provided_count != 1:
                raise ValueError("Please provide exactly one of email or domain")

            if isinstance(role, Enum):
                role_value = role.value
                role_name = role.name.capitalize()
            else:
                role_value = role.lower()
                role_name = role.capitalize()

            if email:
                body = {"type": "user",  "role": role_value, "emailAddress": email}
            elif domain:
                body = {"type": "domain", "role": role_value, "domain": domain}

            result = self.drive.service.permissions().create(fileId=file_id, body=body, fields="*").execute()

            self.drive.print_if_verbose(f"{Fore.GREEN}Added {Fore.RESET}{role_name} {Fore.GREEN}permission for {Fore.RESET}{email or domain} {Fore.GREEN}to {Fore.RESET}{file_id}")
            return result


        def remove(self, file_id, permission_id=None, email=None, domain=None):
            '''
            Remove a permission from a file|folder
            :param file_id: File|folder ID
            :param email: Email address
            :param permission_id: Permission ID
            '''
            provided_args = [permission_id, email, domain]
            provided_count = sum(arg is not None for arg in provided_args)
            if provided_count != 1:
                raise ValueError("Please provide exactly one of permission_id, email, or domain")

            if permission_id:
                pass
            elif email or domain:
                permissions = self.list(file_id=file_id)

                if email:
                    permission = [p for p in permissions if p.get('emailAddress')==email]
                elif domain:
                    permission = [p for p in permissions if p.get('domain') == domain]

                if permission:
                    permission_id = permission[0]['id']

            self.drive.service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
            self.drive.print_if_verbose(f"{Fore.RED}Removed permission of {Fore.RESET}{email or domain or permission_id} {Fore.RED}from {Fore.RESET}{file_id}")

        def transfer_ownership(self, file_id, email):
            '''
            Transfer ownership of a file|folder to an email
            :param file_id: File|folder ID
            :param email: Email address
            :return: Ownership info
            '''
            body = {'type': 'user', 'role': 'owner', 'emailAddress': email}
            result = self.drive.service.permissions().create(fileId=file_id, body=body, transferOwnership=True, fields='*').execute()

            self.drive.print_if_verbose(f"{Fore.BLUE}Transferred ownership of {Fore.RESET}{file_id} {Fore.BLUE}to {Fore.RESET}{email}")

            return result

        def get(self, file_id, permission_id=None, email=None, domain=None):
            '''
            Get permission info
            :param file_id: File|Folder ID
            :param permission_id: Permission ID
            :return:
            '''
            provided_args = [permission_id, email, domain]
            provided_count = sum(arg is not None for arg in provided_args)
            if provided_count != 1:
                raise ValueError("Please provide exactly one of permission_id, email, or domain")

            if permission_id:
                return self.drive.service.permissions().get(fileId=file_id, permissionId=permission_id, fields='*').execute()
            elif email or domain:
                permissions = self.list(file_id=file_id)

                if email:
                    permission = [p for p in permissions if p.get('emailAddress')==email]
                elif domain:
                    permission = [p for p in permissions if p.get('domain') == domain]

                if permission:
                    return permission[0]


        def update(self, file_id, role, permission_id=None, email=None, domain=None):
            provided_args = [permission_id, email, domain]
            provided_count = sum(arg is not None for arg in provided_args)
            if provided_count != 1:
                raise ValueError("Please provide exactly one of permission_id, email, or domain")

            if isinstance(role, Enum):
                role_value = role.value
                role_name = role.name.capitalize()
            else:
                role_value = role.lower()
                role_name = role.capitalize()

            body = {'role': role_value}

            if permission_id:
                pass
            elif email or domain:
                permissions = self.list(file_id=file_id)

                if email:
                    permission = [p for p in permissions if p.get('emailAddress')==email]
                elif domain:
                    permission = [p for p in permissions if p.get('domain') == domain]

                if permission:
                    permission_id = permission[0]['id']

            result = self.drive.service.permissions().update(fileId=file_id, permissionId=permission_id, body=body, fields='*').execute()

            self.drive.print_if_verbose(f"{Fore.BLUE}Updated permission of {Fore.RESET}{email or domain or permission_id}{Fore.BLUE} in file {Fore.RESET}{file_id}{Fore.BLUE} to {Fore.RESET}{role_name}")

            return result

    class Comments:
        def __init__(self, drive):
            self.drive = drive
        def create(self, file_id, content):
            '''
            Create a new comment
            :param file_id: File ID
            :param content: Comment content
            :return:
            '''
            body = {'content': content}
            result = self.drive.service.comments().create(fileId=file_id, body=body, fields='*').execute()

            self.drive.print_if_verbose(f'{Fore.GREEN}Created comment {Fore.RESET}"{content}"{Fore.GREEN} in file {Fore.RESET}{file_id}')

            return result

        def list(self, file_id):
            '''
            List comments of a file
            :param file_id: File ID
            :return: List of comments
            '''
            return self.drive.service.comments().list(fileId=file_id, fields='comments').execute()['comments']

        def get(self, file_id, comment_id):
            '''
            Get a comment info
            :param file_id: File ID
            :param comment_id: Comment ID
            :return: Comment info
            '''
            return self.drive.service.comments().get(fileId=file_id, commentId=comment_id, fields='*').execute()

        def update(self, file_id, comment_id, content):
            '''
            Update a comment
            :param file_id: File ID
            :param comment_id: Comment ID
            :param content: New comment content
            :return: Comment info
            '''
            # resolved not work
            body = {'content': content}
            result = self.drive.service.comments().update(fileId=file_id, commentId=comment_id, body=body, fields='*').execute()
            self.drive.print_if_verbose(f'{Fore.BLUE}Updated comment {Fore.RESET}{comment_id}')
            return result

        def delete(self, file_id, comment_id):
            '''
            Delete a comment
            :param file_id:  File ID
            :param comment_id: Comment ID
            '''
            self.drive.service.comments().delete(fileId=file_id, commentId=comment_id).execute()
            self.drive.print_if_verbose(f"{Fore.RED}Deleted comment {Fore.RESET}{comment_id} in file {file_id}")


    class Replies:
        def __init__(self, drive):
            self.drive = drive

        def create(self, file_id, comment_id, content):
            '''
            Create a reply
            :param file_id: File ID
            :param comment_id: Comment ID
            :param content: Reply content
            :return: Reply info
            '''
            body = {'content': content}
            result = self.drive.service.replies().create(fileId=file_id, commentId=comment_id, body=body, fields='*').execute()
            return result

        def list(self, file_id, comment_id):
            '''
            List replies
            :param file_id: File ID
            :param comment_id: Comment ID
            :return: List of replies
            '''
            return self.drive.service.replies().list(fileId=file_id, commentId=comment_id, fields='replies').execute()['replies']

        def update(self, file_id, comment_id, reply_id, content):
            '''
            Update a reply
            :param file_id: File ID
            :param comment_id: Comment ID
            :param reply_id: Reply ID
            :param content: Reply content
            :return: Reply info
            '''
            body = {'content': content}
            result = self.drive.service.replies().update(fileId=file_id, commentId=comment_id, replyId=reply_id, body=body, fields='*').execute()
            return result

        def get(self, file_id, comment_id, reply_id):
            '''
            Get repy info
            :param file_id: File ID
            :param comment_id: Comment ID
            :param reply_id: Reply ID
            :return: Reply info
            '''
            return self.drive.service.replies().get(fileId=file_id, commentId=comment_id, replyId=reply_id, fields='*').execute()

        def delete(self, file_id, comment_id, reply_id):
            '''
            Delete a reply
            :param file_id: File ID
            :param comment_id: Comment ID
            :param reply_id: Reply ID
            '''
            self.drive.service.replies().delete(fileId=file_id, commentId=comment_id, replyId=reply_id).execute()


    class Revisions:
        def __init__(self, drive):
            self.drive = drive

        def list(self, file_id):
            return self.drive.service.revisions().list(fileId=file_id, fields='revisions').execute()['revisions']

        def get(self, file_id, revision_id):
            return self.drive.service.revisions().get(fileId=file_id, revisionId=revision_id, fields='*').execute()

        def delete(self, file_id, revision_id):
            self.drive.service.revisions().delete(fileId=file_id, revisionId=revision_id).execute()
            self.drive.print_if_verbose(f"{Fore.RED}Deleted revision {Fore.RESET}{revision_id}")