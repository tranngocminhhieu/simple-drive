from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth


class Auth:
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):
        self.auth_info = GoogleAuth()

    @classmethod
    def from_service_account_info(cls, info):
        '''
        Create auth info from a Google service account as dict
        :param info: Google service account as dict
        :return: auth_info
        '''
        instance = cls()
        instance.auth_info.credentials = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict=info, scopes=cls.SCOPES)
        return instance.auth_info

    @classmethod
    def from_service_account_file(cls, file='service_account.json'):
        '''
        Create auth info from a Google service account JSON file
        :param file: Google service account JSON file
        :return: auth_info
        '''
        instance = cls()
        instance.auth_info.credentials = ServiceAccountCredentials.from_json_keyfile_name(filename=file, scopes=cls.SCOPES)
        return instance.auth_info

    @classmethod
    def local_web_server(cls, client_secrets_file='client_secrets.json'):
        '''
        Create auth info using local web and a Client secrets JSON file
        :param client_secrets_file: Client secrets JSON file
        :return: auth_info
        '''
        instance = cls()
        instance.auth_info.DEFAULT_SETTINGS['client_config_file'] = client_secrets_file
        instance.auth_info.LocalWebserverAuth()
        return instance.auth_info
