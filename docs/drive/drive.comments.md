# drive.Comments

## create
```python
drive.Comments.create(file_id, content)
```
Create a new comment.
#### Parameters
- **file_id**: File ID.
- **content**: Comment content.

#### Return
Comment info.

#### Example
```python
drive.Comments.create(file_id='AbcFileId', content='Hello')
```

## get
```python
drive.Comments.get(file_id, comment_id)
```
Get a comment info.
#### Parameters
- **file_id**: File ID.
- **comment_id**: Comment ID.

#### Return
Comment info.

#### Example
```python
drive.Comments.get(file_id='AbcFileId', comment_id='BossCommentId')
```

## update
```python
drive.Comments.update(file_id, comment_id, content)
```
Update a comment.
#### Parameters
- **file_id**: File ID.
- **comment_id**: Comment ID.
- **content**: New comment content.

#### Return
Comment info.

#### Example
```python
drive.Comments.update(file_id='AbcFileId', comment_id='MyCommentId', content='Bye')
```

## list
```python
drive.Comments.list(file_id)
```
List comments of a file.
#### Parameters
- **file_id**: File ID.

#### Return
List of comments.

#### Example
```python
import pandas as pd

comments = drive.Comments.list(file_id='AbcFileId')

df = pd.DataFrame(comments)
```

## delete
```python
drive.Comments.delete(file_id, comment_id)
```
Delete a comment.

#### Parameters
- **file_id**:  File ID.
- **comment_id**: Comment ID.

#### Example
```python
drive.Comments.delete(file_id='AbcFileId', comment_id='MyCommentId')
```