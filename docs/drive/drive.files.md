# drive.Files

## create
```python
drive.Files.create(name, mime_type, dest_folder_id=None)
```

Create a file or folder.

#### Parameters
- **name**: File | folder name.
- **mime_type**: Use `MimeTypes` or visit [https://developers.google.com/drive/api/guides/mime-types](https://developers.google.com/drive/api/guides/mime-types).
- **dest_folder_id**: Destination folder (optional). `None` to create a file in Root.

#### Return
File or folder info.

#### Example
```python
from simple_drive import MimeTypes

drive.Files.create(name='The first folder', mime_type=MimeTypes.FOLDER, dest_folder_id=None)
```

## create_shortcut
```python
drive.Files.create_shortcut(file_id, name=None, dest_folder_id=None)
```
Create a shortcut.

#### Parameters
- **file_id**: Target file ID.
- **shortcut_name**: Shortcut name (optional).
- **dest_folder_id**: Destination folder (optional). `None` to create a shortcut file in the same place with the target file.

#### Return
Shortcut info.

#### Example
```python
drive.Files.create_shortcut(file_id='AbcFileId', name='ABC Shortcut', dest_folder_id=None)
```


## upload
```python
drive.Files.upload(file, dest_folder_id=None, rename=None)
```
Upload a file.

#### Parameters
- **file**: Local file.
- **dest_folder_id**: Destination folder (optional).
- **rename**: Rename file before uploading (optional).

#### Return
File info.

#### Example
```python
drive.Files.upload(file='Excel.xlsx', dest_folder_id='MyFolderId', rename=None)
```

## get
```python
drive.Files.get(file_id, fields='*')
```
Get a file or folder info.

#### Parameters
- **file_id**: File | folder ID.
- **fields**: * is all fields.

#### Return
File | folder info.

#### Example
```python
fields_1 = 'id, name, size, owner'
fields_2 = ['id', 'name', 'size', 'owner']

drive.Files.get(file_id='AbcFileId', fields=fields_1)
```

## move
```python
drive.Files.move(file_id, dest_folder_id)
```
Move a file or folder.

#### Parameters
- **file_id**: File | folder ID.
- **dest_folder_id**: Destination folder.

#### Return
File | folder info.

#### Example
```python
drive.Files.move(file_id='AbcFileId', dest_folder_id='YourFolderId')
```

## copy
```python
drive.Files.copy(file_id, name_prefix='Copy of ', name_suffix=None, dest_folder_id=None)
```

Copy a file. Not support folder yet.

#### Parameters
- **file_id**: File ID.
- **name_prefix**: Default to `'Copy of '`.
- **name_suffix**: Default to `None`.
- **dest_folder_id**: Destination folder (optional). `None` to make a copy in the same place with the original file.

#### Return
File info.

#### Example
```python
drive.Files.copy(file_id='AbcFileId', name_prefix='Backup of ', name_suffix=' (2024-06)', dest_folder_id='BackupFolderId')
```

## rename
```python
drive.Files.rename(file_id, name)
```
Rename a file or folder.

#### Parameters
- **file_id**: File | folder ID.
- **name**: Renamed name.

#### Return
File | folder info.

#### Example
```python
drive.Files.rename(file_id='AbcFileId', name='New name')
```

## restrict
```python
drive.Files.restrict(file_id, read_only=True, owner_restricted=False, reason=None)
```
Restrict the content of a file.

#### Parameters
- **file_id**: File ID.
- **read_only**: `True` or `False`.
- **owner_restricted**: Only the owner of the file can change the restriction status.
- **reason**: Optional.

#### Return
File info.

#### Example
```python
drive.Files.restrict(file_id='AbcFileId', read_only=True, owner_restricted=False, reason='Final contract')
```

## list
```python
drive.Files.list(*args, fields='*', operator='and')
```

List files related to this account.

#### Parameters
- **args**: Use `SearchTerms` or visit [https://developers.google.com/drive/api/guides/ref-search-terms](https://developers.google.com/drive/api/guides/ref-search-terms)
- **operator**: `and`, `or`.

#### Return
List of files.

#### Example
```python
from simple_drive import SearchTerms
import pandas as pd

files = drive.Files.list(SearchTerms.name_contains('Simple'), SearchTerms.createdTime_greater_equal('2024-06-22'), fields='*', operator='and')

df = pd.DataFrame(files)
```

## download
```python
drive.Files.download(file_id, dest_directory=None, get_value=False)
```

Download a file from the Drive.

#### Parameters
- **file_id**: File ID.
- **dest_directory**: Destination directory (optional). `None` to save the file to current directory.
- **get_value**: `False` to save the file, `True` to get the file value only.

#### Return
File value when get_value is `True`.

#### Example
```python
# Save file to local
drive.Files.download(file_id='AbcFileId')

# Get file value, not save to local
file_value = drive.Files.download(file_id='XyzFileId', get_value=True)
```

## export
```python
drive.Files.export(file_id, format='default', dest_directory=None, get_value=False)
```

Export the Google Workspace documents.

#### Parameters
- **file_id**: File ID.
- **format**: xlsx, docx, pdf, pptx, json, csv, etc. Defaults to `'default'` (Sheets:xlsx, Docs:docx, Slides:pptx, Drawings:pdf, AppScript:json). Read more: [https://developers.google.com/drive/api/guides/ref-export-formats](https://developers.google.com/drive/api/guides/ref-export-formats).
- **dest_directory**: Destination directory (optional). `None` to save the file to current directory.
- **get_value**: `False` to save the file, `True` to get the file value only.


#### Return
File value when get_value is `True`.

#### Example
```python
# Export Sheets to Excel
drive.Files.export(file_id='MySheetsId')

# Export Docs to PDF
drive.Files.export(file_id='DocsContractId', format='pdf')
```

## empty_trash

```python
drive.Files.empty_trash()
```
Empty the trash.

## trash
```python
drive.Files.trash(file_id, restore=False)
```
Trash a file or restore a file from trash.

#### Parameters
- **file_id**: File | Folder ID.
- **restore**: `True` to restore, `False` to move to trash.

#### Return
File info.

#### Example
```python
# Move to trash
drive.Files.trash(file_id='AbcFileId', restore=False)

# Restore from trash
drive.Files.trash(file_id='AbcFileId', restore=True)
```

## delete
```python
drive.Files.delete(file_id)
```
Delete a file or folder.

#### Parameters
- **file_id**: File | folder ID.

#### Example
```python
drive.Files.delete(file_id='AbcFileId')
```