# simple-drive
[![Downloads](https://img.shields.io/pypi/dm/simple-drive)](https://pypi.org/project/simple-drive)
[![Pypi](https://img.shields.io/pypi/v/simple-drive?label=pip&logo=PyPI&logoColor=white)](https://pypi.org/project/simple-drive)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/tranngocminhhieu/simple-drive/issues)
[![MIT](https://img.shields.io/github/license/tranngocminhhieu/simple-drive)](https://github.com/tranngocminhhieu/simple-drive/blob/main/LICENSE)


Use Google Drive API in the simplest way

## Installation
### Install from GitHub
```shell
pip install --upgrade git+https://github.com/tranngocminhhieu/simple-drive.git
```
### Install from PyPI
```shell
pip install --upgrade simple-drive
```

## Usage
### Import
```python
from simple_drive import Drive, Auth, MimeTypes, Roles
```

### Create auth info
#### From a service account
Read more: [How to create a Service Account](https://lucidgen.com/en/create-service-account-and-enable-google-cloud-api/)
```python
# Way 1
auth = Auth.from_service_account_file(file=YOUR_SERVICE_ACCOUNT_FILE)
# Way 2
auth = Auth.from_service_account_info(info=YOUR_SERVICE_ACCOUNT_INFO)
```
#### From local web server
```python
auth = Auth.local_web_server(client_secrets_file=YOUR_CLIENT_SECRETS_FILE)
```

### Use Drive API
```python
drive = Drive(auth=auth, verbose=True)
```

#### Create a file or folder
```python
# mime_type = MimeTypes.FOLDER
# mime_type = MimeTypes.SHEETS
# ...
drive.create(name, mime_type, dest_folder_id=None)
```

#### Delete a file or folder
```python
drive.delete(file_id)
```

#### Move a file or folder
```python
drive.move(file_id, dest_folder_id)
```

#### Upload a file
```python
drive.upload(file, dest_folder_id=None, rename=None)
```

#### Copy a file
Not support folder yet.
```python
drive.copy(file_id, name_prefix='Copy of ', name_suffix=None, dest_folder_id=None)
```

#### Rename a file or folder
```python
drive.rename(file_id, name)
```

#### Get a file or folder info
```python
drive.get_file_info(file_id, fields='*')
```

#### Export the Google Workspace documents
```python
drive.export(file_id, format='default', dest_directory=None, get_value=False)
```

#### Download a file
```python
drive.download(file_id, dest_directory=None, get_value=False)
```

#### List files related to this account
```python
drive.list_files(name_contains=None, owner_email=None, writer_email=None, reader_email=None, folder_id=None, trashed=None, mime_type_contains=None, shared_with_me=None, visibility=None, custom_filter=None)
```

#### Get the account storage quota
```python
drive.get_storage_quota()
```

#### Empty trash
```python
drive.empty_trash()
```

#### Move a file to trash or restore a file from trash
```python
drive.trash(file_id, restore=False)
```

#### Create a shortcut
```python
drive.create_shortcut(file_id, shortcut_name=None, dest_folder_id=None)
```

#### Get permission of a file or folder
```python
drive.list_permissions(file_id)
```

#### Add permission to a file or folder
We can provide `email` or `domain` or both.
```python
# role = Roles.VIEWER
# role = Roles.EDITOR
# role = Roles.COMMENTER
drive.add_permission(file_id, role, email=None, domain=None)
```

#### Remove a permission from a file or folder
We can provide `permission_id` or `email` or `domain` or all.
```python
drive.remove_permission(file_id, permission_id=None, email=None, domain=None)
```

#### Transfer ownership of a file or folder to an email
Support emails in organization.
```python
drive.transfer_ownership(file_id, email)
```

## Conclusion
I welcome your contributions!