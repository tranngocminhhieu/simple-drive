from colorama import Fore


class Revisions:
    def __init__(self, drive):
        self.drive = drive

    def get(self, file_id, revision_id):
        '''
        Get revision info
        :param file_id: File ID
        :param revision_id: Revision ID
        :return: Revision info
        '''
        return self.drive.service.revisions().get(fileId=file_id, revisionId=revision_id, fields='*').execute()

    def list(self, file_id):
        '''
        List all revisions
        :param file_id: File ID
        :return: List of revisions
        '''
        return self.drive.service.revisions().list(fileId=file_id, fields='revisions').execute()['revisions']

    def delete(self, file_id, revision_id):
        '''
        Delete a revision
        :param file_id: File ID
        :param revision_id: Revision ID
        '''
        self.drive.service.revisions().delete(fileId=file_id, revisionId=revision_id).execute()
        self.drive.print_if_verbose(f"{Fore.RED}Deleted revision {Fore.RESET}{revision_id}")