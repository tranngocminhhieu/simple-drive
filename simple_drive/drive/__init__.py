from colorama import Fore
from googleapiclient.discovery import build
from pydrive2.drive import GoogleDrive

from .comments import Comments
from .files import Files
from .permissions import Permissions
from .replies import Replies
from .revisions import Revisions
from .about import About

class Drive:
    def __init__(self, auth, verbose=True):
        '''
        Use Google Drive API in the simplest way
        :param auth_info: Use Auth class to authenticate with Google Drive
        :param verbose: Print result
        '''
        self.verbose = verbose

        # For Upload
        self.google_drive = GoogleDrive(auth)

        # For other features
        self.service = build(serviceName='drive', version='v3', credentials=auth.credentials)

        self.Files = Files(drive=self)
        self.Comments = Comments(drive=self)
        self.Permissions = Permissions(drive=self)
        self.Replies = Replies(drive=self)
        self.Revisions = Revisions(drive=self)
        self.About = About(drive=self)

    # Support
    def print_if_verbose(self, *args):
        if self.verbose:
            print(*args)