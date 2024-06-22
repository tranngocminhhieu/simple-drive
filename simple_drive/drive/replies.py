from colorama import Fore


class Replies:
    def __init__(self, drive):
        self.drive = drive


    def create(self, file_id, comment_id, content):
        '''
        Create a reply.
        :param file_id: File ID.
        :param comment_id: Comment ID.
        :param content: Reply content.
        :return: Reply info.
        '''
        body = {'content': content}
        result = self.drive.service.replies().create(fileId=file_id, commentId=comment_id, body=body, fields='*').execute()

        if len(content) > 20:
            truncated_content = content[:20] + '...'
        else:
            truncated_content = content
        self.drive.print_if_verbose(f'{Fore.GREEN}Replied {Fore.RESET}"{truncated_content}"{Fore.GREEN} to comment {Fore.RESET}{comment_id}')
        return result


    def get(self, file_id, comment_id, reply_id):
        '''
        Get repy info.
        :param file_id: File ID.
        :param comment_id: Comment ID.
        :param reply_id: Reply ID.
        :return: Reply info.
        '''
        return self.drive.service.replies().get(fileId=file_id, commentId=comment_id, replyId=reply_id, fields='*').execute()


    def update(self, file_id, comment_id, reply_id, content):
        '''
        Update a reply.
        :param file_id: File ID.
        :param comment_id: Comment ID.
        :param reply_id: Reply ID.
        :param content: Reply content.
        :return: Reply info.
        '''
        body = {'content': content}
        result = self.drive.service.replies().update(fileId=file_id, commentId=comment_id, replyId=reply_id, body=body, fields='*').execute()

        if len(content) > 20:
            truncated_content = content[:20] + '...'
        else:
            truncated_content = content
        self.drive.print_if_verbose(f'{Fore.BLUE}Updated the content of reply {Fore.RESET}{reply_id}{Fore.BLUE} to {Fore.RESET}"{truncated_content}"')
        return result


    def list(self, file_id, comment_id):
        '''
        List replies.
        :param file_id: File ID.
        :param comment_id: Comment ID.
        :return: List of replies.
        '''
        return self.drive.service.replies().list(fileId=file_id, commentId=comment_id, fields='replies').execute()['replies']


    def delete(self, file_id, comment_id, reply_id):
        '''
        Delete a reply.
        :param file_id: File ID.
        :param comment_id: Comment ID.
        :param reply_id: Reply ID.
        '''
        self.drive.service.replies().delete(fileId=file_id, commentId=comment_id, replyId=reply_id).execute()
        self.drive.print_if_verbose(f"{Fore.RED}Deleted reply {Fore.RESET}{reply_id} on file {file_id}")
