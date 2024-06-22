# drive.Files

## create
Create a file or folder.

Use `MimeTypes` or visit https://developers.google.com/drive/api/guides/mime-types.

```python
from simple_drive import MimeTypes

# mime_type = MimeTypes.FOLDER
# mime_type = mime_type.SHEETS
# ...
drive.Files.create(name, mime_type, dest_folder_id=None)
```

    :param name: File|folder name
    :param mime_type: Use MimeTypes or visit https://developers.google.com/drive/api/guides/mime-types
    :param dest_folder_id: Destination folder
    :return: File|folder info


## create_shortcut
 Create a shortcut.

```python
drive.Files.create_shortcut(file_id, name=None, dest_folder_id=None)
```
    :param file_id: File ID
    :param shortcut_name: Shortcut name
    :param dest_folder_id: Destination folder
    :return: Shortcut info



## upload
Upload a file.

```python
drive.Files.upload(file, dest_folder_id=None, rename=None)
```

    :param file: Local file
    :param dest_folder_id: Destination folder
    :param rename: Rename file before uploading
    :return: File info

## get
Get a file or folder info.

```python
drive.Files.get(file_id, fields='*')
```

    :param file_id: File|folder ID
    :param fields: * is all fields
    :return: File|folder info
    


## move
Move a file or folder.

```python
drive.Files.move(file_id, dest_folder_id)
```

    :param file_id: File|folder ID
    :param dest_folder_id: Destination folder
    :return: File|folder info

## copy
Copy a file. Not support folder yet.

```python
drive.Files.copy(file_id, name_prefix='Copy of ', name_suffix=None, dest_folder_id=None)
```

    :param file_id: File ID
    :param name_prefix: Default to 'Copy of '
    :param name_suffix: Default to ''
    :param dest_folder_id: Destination folder
    :return: File info

## rename
Rename a file or folder.

```python
drive.Files.rename(file_id, name)
```

    :param file_id: File|folder ID
    :param name: Renamed name
    :return: File|folder info


## restrict
Restrict the content of a file.
```python
drive.Files.restrict(file_id, read_only=True, owner_restricted=False, reason=None)
```

    :param file_id: File ID
    :param read_only: True or False
    :param owner_restricted: Only the owner of the file can change the restriction status
    :param reason: Optional
    :return: File info

## list
List files related to this account.
```python
drive.Files.list(*args, fields='*', operator='and')
```

    :param args: Use SearchTerms or visit https://developers.google.com/drive/api/guides/ref-search-terms
    :param operator: and, or
    :return: List of files

## download
Download a file from the Drive.
```python
drive.Files.download(file_id, dest_directory=None, get_value=False)
```

    :param file_id: File ID
    :param dest_directory: Destination directory
    :param get_value: False to save the file, True to get the file value only
    :return: file value when get_value is True

## export
Export the Google Workspace documents.
```python
drive.Files.export(file_id, format='default', dest_directory=None, get_value=False)
```

    :param file_id: File ID
    :param format: Format of the exported file (xlsx, docx, pdf, pptx, json, csv, ...), defaults to 'default'. Read more: https://developers.google.com/drive/api/guides/ref-export-formats")
    :param dest_directory: Destination directory
    :param get_value: False to save the file, True to get the file value only
    :return: file value when get_value is True

## empty_trash
Empty the trash.
```python
drive.Files.empty_trash()
```

## trash
Trash a file or restore a file from trash.
```python
drive.Files.trash(file_id, restore=False)
```

    :param file_id: File|Folder ID
    :param restore: True to restore, False to move to trash

## delete
Delete a file or folder.
```python
drive.Files.delete(file_id)
```

    :param file_id: File|folder ID