# drive.Files

## create

```python
drive.Files.create(name, mime_type, dest_folder_id=None)
```

## create_shortcut

```python
drive.Files.create_shortcut(file_id, name=None, dest_folder_id=None)
```

## upload

```python
drive.Files.upload(file, dest_folder_id=None, rename=None)
```

## get
```python
drive.Files.get(file_id, fields='*')
```

## move
```python
drive.Files.move(file_id, dest_folder_id)
```

## copy
```python
drive.Files.copy(file_id, name_prefix='Copy of ', name_suffix=None, dest_folder_id=None)
```

## rename
```python
drive.Files.rename(file_id, name)
```

## restrict
```python
drive.Files.restrict(file_id, read_only=True, owner_restricted=False, reason=None)
```

## list
```python
drive.Files.list(*args, fields='*', operator='and')
```

## download
```python
drive.Files.download(file_id, dest_directory=None, get_value=False)
```

## export
```python
drive.Files.export(file_id, format='default', dest_directory=None, get_value=False)
```

## empty_trash
```python
drive.Files.empty_trash()
```

## trash
```python
drive.Files.trash(file_id, restore=False)
```

## delete
```python
drive.Files.delete(file_id)
```