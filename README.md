# simple-drive
[![Downloads](https://img.shields.io/pypi/dm/simple-drive)](https://pypi.org/project/simple-drive)
[![Pypi](https://img.shields.io/pypi/v/simple-drive?label=pip&logo=PyPI&logoColor=white)](https://pypi.org/project/simple-drive)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/tranngocminhhieu/simple-drive/issues)
[![MIT](https://img.shields.io/github/license/tranngocminhhieu/simple-drive)](https://github.com/tranngocminhhieu/simple-drive/blob/main/LICENSE)

![simple-drive.jpg](https://raw.githubusercontent.com/tranngocminhhieu/simple-drive/main/docs/simple-drive.jpg)

This package is designed to make it easier for Python users to utilize the Google Drive API. The syntax is concise and easy to understand, and it was developed based on the [Google Drive API documentation](https://developers.google.com/drive/api/).

## Main features

### Files
- create
- create_shortcut
- upload
- get
- move
- copy
- rename
- restrict
- list
- download
- export
- empty_trash
- trash
- delete

### Perissions
- add
- transfer_ownership
- get
- update
- list
- remove

### Comments
- create
- get
- update
- list
- delete

### Replies
- create
- get
- update
- list
- delete

### Revisions
- get
- list
- delete

## Installation
### Install from GitHub
```shell
pip install --upgrade git+https://github.com/tranngocminhhieu/simple-drive.git
```
### Install from PyPI
```shell
pip install --upgrade simple-drive
```

##  User manual

Please read the [Documents](https://tranngocminhhieu.gitbook.io/simple-drive).

Quick start example:

```python
from simple_drive import Auth, Drive, MimeTypes, Roles

# Authorize with a service account
auth = Auth.from_service_account_file(file='service_account.json')

# Drive object
drive = Drive(auth=auth, verbose=True)

# Create a folder
folder = drive.Files.create(name='Example folder', mime_type=MimeTypes.FOLDER, dest_folder_id=None)

# Add editor permission for someone
drive.Permissions.add(file_id=folder['id'], email='her@gmail.com', role=Roles.EDITOR)

# ...
```

---

I welcome your contributions!