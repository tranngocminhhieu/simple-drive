# drive.Permissions

## add
```python
drive.Permissions.add(file_id, role, email=None, domain=None)
```
Add permission to a file or folder. Please provide exactly one of `email` or `domain`.
#### Parameters
- **file_id**: File | folder ID.
- **role**: Use `Roles` or visit [https://developers.google.com/drive/api/guides/ref-roles](https://developers.google.com/drive/api/guides/ref-roles).
- **email**: Email address.
- **domain**: Domain, e.g. google.com.

#### Return
Permission info.

#### Example
```python
from simple_drive import Roles

# Add editor permission for an email
drive.Permissions.add(file_id='AbcFileId', role=Roles.EDITOR, email='your@gmail.com')

# Add viewer permission for a domain
drive.Permissions.add(file_id='AbcFileId', role=Roles.VIEWER, domain='domain.com')
```

## transfer_ownership
```python
drive.Permissions.transfer_ownership(file_id, email)
```
Transfer ownership of a file or folder to an email.
#### Parameters
- **file_id**: File | folder ID.
- **email**: Email address.

#### Return
Ownership info.

#### Example
```python
drive.Permissions.transfer_ownership(file_id='AbcFileId', email='her@domain.com')
```

## get
```python
drive.Permissions.get(file_id, permission_id=None, email=None, domain=None)
```
Get permission info. Please provide exactly one of `permission_id`, `email`, or `domain`.
#### Parameters
- file_id: File | Folder ID.
- permission_id: Permission ID.

#### Return
Permission info.

#### Example
```python
drive.Permissions.get(file_id='AbcFileId', email='your@gmail.com')
```

## update
```python
drive.Permissions.update(file_id, role, permission_id=None, email=None, domain=None)
```
Update a permission. Please provide exactly one of `permission_id`, `email`, or `domain`.
#### Parameters
- **file_id**: File ID.
- **role**: Use `Roles` or visit [https://developers.google.com/drive/api/guides/ref-roles](https://developers.google.com/drive/api/guides/ref-roles).
- **permission_id**: Permission ID.
- **email**: Email address.
- **domain**: Domain, e.g. google.com.

#### Return
Permission info.

#### Example
```python
from simple_drive import Roles

drive.Permissions.update(file_id='AbcFileId', role=Roles.COMMENTER, email='her@gmail.com')
```

## list
```python
drive.Permissions.list(file_id)
```
Get a list of permissions of a file or folder.
#### Parameters
- **file_id**: File | folder ID.

#### Return
Permission info.

#### Example
```python
drive.Permissions.list(file_id='AbcFileId')
```

## remove
```python
drive.Permissions.remove(file_id, permission_id=None, email=None, domain=None)
```
Remove a permission from a file | folder. Please provide exactly one of `permission_id`, `email`, or `domain`.
#### Parameters
- **file_id**: File | folder ID.
- **email**: Email address.
- **permission_id**: Permission ID.

#### Example
```python
drive.Permissions.remove(file_id='AbcFileId', email='her@gmail.com')
```