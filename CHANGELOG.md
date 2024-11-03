# CHANGELOG

## 2.0.5
- Improve code in Drive.Permissions.

## 2.0.4
- Drive.Files: Support list files in deep folders with param `deep_folder`.

## 2.0.3
- Drive.Permissions: Support transfer ownership with gmail.com.

## 2.0.2
- Drive.Permissions: Fix wrong detect args (email, domain, anyone, ...).

## 2.0.1
- Drive.Permissions: Add anyone argument to functions.

## 2.0.0 (Big Update)

### drive.About
- get
- get_storage_quota

### drive.Files
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

### drive.Permissions
- add
- transfer_ownership
- get
- update
- list
- remove

### drive.Comments
- create
- get
- update
- list
- delete

### drive.Replies
- create
- get
- update
- list
- delete

### Drive.Revisions
- get
- list
- delete

## constants.py
- Add `SearchTerms` class


## 1.0.2
- Improve micro things

## 1.0.1
- `Drive().remove_permission` make sure email is lower case.
- Clean code.
- Human readable log for `get_storage_quota`

## 1.0.0
Drive functions:
- create
- delete
- move
- upload
- get_file_info
- copy
- rename
- list_files
- get_storage_quota
- list_permissions
- add_permission
- remove_permission
- transfer_ownership

Auth functions:
- from_service_account_info
- from_service_account_file
- local_web_server

constants:
- Roles
- MimeTypes