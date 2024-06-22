from colorama import Fore


class Comments:
    def __init__(self, drive):
        self.drive = drive

    def create(self, file_id, content):
        '''
        Create a new comment.
        :param file_id: File ID.
        :param content: Comment content.
        :return: Comment info.
        '''
        body = {'content': content}
        result = self.drive.service.comments().create(fileId=file_id, body=body, fields='*').execute()

        if len(content) > 20:
            truncated_content = content[:20] + '...'
        else:
            truncated_content = content
        self.drive.print_if_verbose(f'{Fore.GREEN}Commented {Fore.RESET}"{truncated_content}"{Fore.GREEN} on file {Fore.RESET}{file_id}')

        return result

    def get(self, file_id, comment_id):
        '''
        Get a comment info.
        :param file_id: File ID.
        :param comment_id: Comment ID.
        :return: Comment info.
        '''
        return self.drive.service.comments().get(fileId=file_id, commentId=comment_id, fields='*').execute()

    def update(self, file_id, comment_id, content):
        '''
        Update a comment.
        :param file_id: File ID.
        :param comment_id: Comment ID.
        :param content: New comment content.
        :return: Comment info.
        '''
        # resolved not work
        body = {'content': content}
        result = self.drive.service.comments().update(fileId=file_id, commentId=comment_id, body=body, fields='*').execute()

        if len(content) > 20:
            truncated_content = content[:20] + '...'
        else:
            truncated_content = content
        self.drive.print_if_verbose(f'{Fore.BLUE}Updated the content of comment {Fore.RESET}{comment_id}{Fore.BLUE} to {Fore.RESET}"{truncated_content}"')
        return result

    def list(self, file_id):
        '''
        List comments of a file.
        :param file_id: File ID.
        :return: List of comments.
        '''
        return self.drive.service.comments().list(fileId=file_id, fields='comments').execute()['comments']

    def delete(self, file_id, comment_id):
        '''
        Delete a comment.
        :param file_id:  File ID.
        :param comment_id: Comment ID.
        '''
        self.drive.service.comments().delete(fileId=file_id, commentId=comment_id).execute()
        self.drive.print_if_verbose(f"{Fore.RED}Deleted comment {Fore.RESET}{comment_id} on file {file_id}")
