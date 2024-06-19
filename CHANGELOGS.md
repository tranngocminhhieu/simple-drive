# 1.0.1
- `Drive().remove_permission` make sure email is lower case.
- Clean code.
- Human readable log for `get_storage_quota`

# 1.0.0
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