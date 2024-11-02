import io
import os
import os.path
from enum import Enum

from colorama import Fore
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from ..constants import MimeTypes


class Files:
    def __init__(self, drive):
        self.drive = drive
        self.default_file_fields = 'id, name, mimeType, size, parents, webViewLink, owners'

    def create(self, name, mime_type, dest_folder_id=None):
        '''
        Create a file or folder.
        :param name: File | folder name.
        :param mime_type: Use MimeTypes or visit https://developers.google.com/drive/api/guides/mime-types.
        :param dest_folder_id: Destination folder (optional). None to create a file in Root.
        :return: File or folder info.
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

        self.drive.print_if_verbose(
            f"{Fore.GREEN}Created {'an' if mime_type_name[0].lower() in 'ueoai' else 'a'} {mime_type_name} as {Fore.RESET}{name}{f'{Fore.GREEN} in folder {Fore.RESET}{dest_folder_id}' if dest_folder_id else ''}")

        return file

    def create_shortcut(self, file_id, name=None, dest_folder_id=None):
        '''
        Create a shortcut.
        :param file_id: Target file ID.
        :param shortcut_name: Shortcut name (optional).
        :param dest_folder_id: Destination folder (optional). None to create a shortcut file in the same place with the target file.
        :return: Shortcut info.
        '''
        if not name:
            name = self.get(file_id=file_id).get('name')

        shortcut_metadata = {
            'Name': name,
            'mimeType': MimeTypes.SHORTCUT.value,
            'shortcutDetails': {
                'targetId': file_id
            }
        }

        if dest_folder_id:
            shortcut_metadata['parents'] = [dest_folder_id]

        shortcut = self.drive.service.files().create(body=shortcut_metadata,
                                                     fields=f'{self.default_file_fields},shortcutDetails').execute()

        self.drive.print_if_verbose(f"{Fore.GREEN}Created a shortcut of {Fore.RESET}{file_id}{Fore.GREEN} as {Fore.RESET}{name}")
        return shortcut

    def upload(self, file, dest_folder_id=None, rename=None):
        '''
        Upload a file.
        :param file: Local file.
        :param dest_folder_id: Destination folder (optional).
        :param rename: Rename file before uploading (optional).
        :return: File info.
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

        self.drive.print_if_verbose(
            f"{Fore.GREEN}Uploaded {Fore.RESET}{title}{f'{Fore.GREEN} to folder {Fore.RESET}{dest_folder_id}' if dest_folder_id else ''}")

        return new_file

    def get(self, file_id, fields='*'):
        '''
        Get a file or folder info.
        :param file_id: File | folder ID.
        :param fields: * is all fields.
        :return: File | folder info.
        '''
        if isinstance(file_id, list):
            fields = ', '.join(fields)
        return self.drive.service.files().get(fileId=file_id, fields=fields).execute()

    def move(self, file_id, dest_folder_id):
        '''
        Move a file or folder.
        :param file_id: File | folder ID.
        :param dest_folder_id: Destination folder.
        :return: File|folder info.
        '''
        file = self.drive.service.files().get(fileId=file_id, fields=self.default_file_fields).execute()
        remove_parents = file['parents'][0]
        result = self.drive.service.files().update(fileId=file_id,
                                                   addParents=dest_folder_id,
                                                   removeParents=remove_parents,
                                                   fields=self.default_file_fields).execute()

        self.drive.print_if_verbose(
            f"{Fore.BLUE}Moved {Fore.RESET}{result.get('name', file_id)}{Fore.BLUE} to folder {Fore.RESET}{dest_folder_id}")

        return result

    def copy(self, file_id, name_prefix='Copy of ', name_suffix=None, dest_folder_id=None):
        '''
        Copy a file. Not support folder yet.
        :param file_id: File ID.
        :param name_prefix: Default to 'Copy of '.
        :param name_suffix: Default to None.
        :param dest_folder_id: Destination folder (optional). None to make a copy in the same place with the original file.
        :return: File info.
        '''
        current_file = self.drive.service.files().get(fileId=file_id, fields=self.default_file_fields).execute()
        current_name = current_file['name']
        new_name = f"{name_prefix if name_prefix else ''}{current_name}{name_suffix if name_suffix else ''}"

        body = {'name': new_name}
        if dest_folder_id:
            body['parents'] = [dest_folder_id]

        new_file = self.drive.service.files().copy(fileId=file_id, body=body,
                                                   fields=self.default_file_fields).execute()

        self.drive.print_if_verbose(
            f"{Fore.GREEN}Copied {Fore.RESET}{current_name}{Fore.GREEN} to {Fore.RESET}{new_name}{f'{Fore.GREEN} in folder {Fore.RESET}{dest_folder_id}' if dest_folder_id else ''}")

        return new_file

    def rename(self, file_id, name):
        '''
        Rename a file or folder.
        :param file_id: File | folder ID.
        :param name: Renamed name.
        :return: File | folder info.
        '''
        body = {'name': name}
        result = self.drive.service.files().update(fileId=file_id, body=body,
                                                   fields=self.default_file_fields).execute()
        self.drive.print_if_verbose(f"{Fore.BLUE}Renamed {Fore.RESET}{file_id} {Fore.BLUE}to {Fore.RESET}{name}")
        return result

    def restrict(self, file_id, read_only=True, owner_restricted=False, reason=None):
        '''
        Restrict the content of a file.
        :param file_id: File ID.
        :param read_only: True or False.
        :param owner_restricted: Only the owner of the file can change the restriction status.
        :param reason: Optional.
        :return: File info.
        '''
        content_restriction = {'readOnly': read_only, 'ownerRestricted': owner_restricted}
        if reason:
            content_restriction['reason'] = reason

        result = self.drive.service.files().update(fileId=file_id,
                                                   body={'contentRestrictions': [content_restriction]},
                                                   fields=f"{self.default_file_fields},contentRestrictions").execute();

        self.drive.print_if_verbose(f"{Fore.BLUE}Updated content restriction for {Fore.RESET}{file_id}")

        return result

    def list(self, *args, fields='*', operator='and', deep_folder=False):
        '''
        List files related to this account.
        :param args: Use SearchTerms or visit https://developers.google.com/drive/api/guides/ref-search-terms.
        :param operator: and, or.
        :return: List of files.
        '''

        filters = [*args]
        param = f" {operator} ".join(filters) if len(filters) else None

        if isinstance(fields, list):
            fields = ', '.join(fields)

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
                        fields=f"nextPageToken, files({fields})",
                        pageToken=page_token,
                    )
                    .execute()
                )
                for file in response.get("files", []):
                    # Process change
                    self.drive.print_if_verbose(f"Found file: {Fore.BLUE}{file.get('name')}{Fore.RESET} | {file.get('id')}")

                    # Support deep
                    if deep_folder and file['mimeType'] == 'application/vnd.google-apps.folder':
                        files.extend(self.list(f"'{file['id']}' in parents", deep_folder=True))

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
        Download a file from the Drive.
        :param file_id: File ID.
        :param dest_directory: Destination directory (optional). None to save the file to current directory.
        :param get_value: False to save the file, True to get the file value only.
        :return: File value when get_value is True.
        '''

        # https://developers.google.com/drive/api/guides/manage-downloads
        try:
            request = self.drive.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                self.drive.print_if_verbose(f"Download {int(status.progress() * 100)}.")

            if not get_value:
                file_info = self.get(file_id)

                if dest_directory:
                    name = os.path.join(dest_directory, file_info.get('name'))
                else:
                    name = file_info.get('name')

                with open(name, 'wb') as f:
                    f.write(file.getvalue())

                self.drive.print_if_verbose(f"{Fore.GREEN}Saved {Fore.RESET}{file_id}{Fore.GREEN} as {Fore.RESET}{name}")

            else:
                self.drive.print_if_verbose(f"{Fore.GREEN}Got value of {Fore.RESET}{file_id}")
                return file.getvalue()

        except HttpError as error:
            print(f"An error occurred: {error}")


    def export(self, file_id, format='default', dest_directory=None, get_value=False):
        '''
        Export the Google Workspace documents.
        :param file_id: File ID
        :param format: xlsx, docx, pdf, pptx, json, csv, etc. Defaults to 'default' (Sheets:xlsx, Docs:docx, Slides:pptx, Drawings:pdf, AppScript:json). Read more: https://developers.google.com/drive/api/guides/ref-export-formats.
        :param dest_directory: Destination directory (optional). None to save the file to current directory.
        :param get_value: False to save the file, True to get the file value only,
        :return: File value when get_value is True.
        '''

        # Prepare export mimeType and format (file mimeType is different with export mimeType)
        file_info = self.get(file_id=file_id)
        export_formats = {file_info['exportLinks'][v].split('=')[-1]: v for v in file_info['exportLinks']}
        file_mime_type = file_info.get('mimeType')

        format = format.lower()
        if format not in export_formats and format != 'default':
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


            if not get_value:
                if dest_directory:
                    name = os.path.join(dest_directory, f"{file_info.get('name')}.{format}")
                else:
                    name = f"{file_info.get('name')}.{format}"

                with open(name, 'wb') as f:
                    f.write(file.getvalue())

                self.drive.print_if_verbose(f"{Fore.GREEN}Saved {Fore.RESET}{file_id}{Fore.GREEN} as {Fore.RESET}{name}")

            else:
                self.drive.print_if_verbose(f"{Fore.GREEN}Got value of {Fore.RESET}{file_id}")
                return file.getvalue()


        except HttpError as error:
            print(f"An error occurred: {error}")


    def empty_trash(self):
        '''
        Empty the trash.
        '''
        self.drive.service.files().emptyTrash().execute()
        self.drive.print_if_verbose(f"{Fore.YELLOW}Emptied the trash{Fore.RESET}")

    def trash(self, file_id, restore=False):
        '''
        Trash a file or restore a file from trash.
        :param file_id: File | Folder ID.
        :param restore: True to restore, False to move to trash.
        :return: File info.
        '''
        body = {'trashed': not restore}
        result = self.drive.service.files().update(fileId=file_id, body=body,
                                                   fields=self.default_file_fields).execute()
        if restore:
            self.drive.print_if_verbose(
                f"{Fore.GREEN}Restored {Fore.RESET}{file_id}{Fore.GREEN} from trash{Fore.RESET}")
        else:
            self.drive.print_if_verbose(f"{Fore.YELLOW}Moved {Fore.RESET}{file_id}{Fore.YELLOW} to trash{Fore.RESET}")
        return result

    def delete(self, file_id):
        '''
        Delete a file or folder.
        :param file_id: File | folder ID.
        '''
        self.drive.service.files().delete(fileId=file_id).execute()
        self.drive.print_if_verbose(f"{Fore.RED}Deleted {Fore.RESET}{file_id}")
