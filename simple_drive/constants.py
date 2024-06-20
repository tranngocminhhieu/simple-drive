from enum import Enum

class Roles(Enum):
    VIEWER = 'reader'
    EDITOR = 'writer'
    COMMENTER = 'commenter'


class MimeTypes(Enum):
    # https://developers.google.com/drive/api/guides/mime-types
    AUDIO = 'application/vnd.google-apps.audio'
    DOCS = 'application/vnd.google-apps.document'
    THIRD_PARTY_SHORTCUT = 'application/vnd.google-apps.drive-sdk'
    DRAWINGS = 'application/vnd.google-apps.drawing'
    FILE = 'application/vnd.google-apps.file'
    FOLDER = 'application/vnd.google-apps.folder'
    FORMS = 'application/vnd.google-apps.form'
    FUSION_TABLES = 'application/vnd.google-apps.fusiontable'
    JAMBOARD = 'application/vnd.google-apps.jam'
    EMAIL_LAYOUT = 'application/vnd.google-apps.mail-layout'
    MY_MAPS = 'application/vnd.google-apps.map'
    PHOTOS = 'application/vnd.google-apps.photo'
    SLIDES = 'application/vnd.google-apps.presentation'
    APPS_SCRIPT = 'application/vnd.google-apps.script'
    SHORTCUT = 'application/vnd.google-apps.shortcut'
    SITES = 'application/vnd.google-apps.site'
    SHEETS = 'application/vnd.google-apps.spreadsheet'
    UNKNOWN = 'application/vnd.google-apps.unknown'
    VIDEO = 'application/vnd.google-apps.video'
    XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    PPTX = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    PDF = 'application/pdf'
    JSON = 'application/vnd.google-apps.script+json'

class SearchTerms:
    @staticmethod
    def name_contains(value: str) -> str:
        return f"name contains '{value}'"

    @staticmethod
    def name_equal(value: str) -> str:
        return f"name = '{value}'"

    @staticmethod
    def name_not_equal(value: str) -> str:
        return f"name != '{value}'"

    @staticmethod
    def fullText_contains(value: str) -> str:
        return f"fullText contains '{value}'"

    @staticmethod
    def mimeType_contains(value: str) -> str:
        '''
        :param value: Use MimeTypes or visit https://developers.google.com/drive/api/guides/mime-types
        '''
        if isinstance(value, Enum):
            value = value.value
        return f"mimeType contains '{value}'"

    @staticmethod
    def mimeType_equal(value: str) -> str:
        '''
        :param value: Use MimeTypes or visit https://developers.google.com/drive/api/guides/mime-types
        '''
        if isinstance(value, Enum):
            value = value.value
        return f"mimeType = '{value}'"

    @staticmethod
    def mimeType_not_equal(value: str) -> str:
        '''
        :param value: Use MimeTypes or visit https://developers.google.com/drive/api/guides/mime-types
        '''
        if isinstance(value, Enum):
            value = value.value
        return f"mimeType != '{value}'"

    @staticmethod
    def modifiedTime_less_than(value: str) -> str:
        return f"modifiedTime < '{value}'"

    @staticmethod
    def modifiedTime_less_equal(value: str) -> str:
        return f"modifiedTime <= '{value}'"

    @staticmethod
    def modifiedTime_equal(value: str) -> str:
        return f"modifiedTime = '{value}'"

    @staticmethod
    def modifiedTime_not_equal(value: str) -> str:
        return f"modifiedTime != '{value}'"

    @staticmethod
    def modifiedTime_greater_than(value: str) -> str:
        return f"modifiedTime > '{value}'"

    @staticmethod
    def modifiedTime_greater_equal(value: str) -> str:
        return f"modifiedTime >= '{value}'"

    @staticmethod
    def viewedByMeTime_less_than(value: str) -> str:
        return f"viewedByMeTime < '{value}'"

    @staticmethod
    def viewedByMeTime_less_equal(value: str) -> str:
        return f"viewedByMeTime <= '{value}'"

    @staticmethod
    def viewedByMeTime_equal(value: str) -> str:
        return f"viewedByMeTime = '{value}'"

    @staticmethod
    def viewedByMeTime_not_equal(value: str) -> str:
        return f"viewedByMeTime != '{value}'"

    @staticmethod
    def viewedByMeTime_greater_than(value: str) -> str:
        return f"viewedByMeTime > '{value}'"

    @staticmethod
    def viewedByMeTime_greater_equal(value: str) -> str:
        return f"viewedByMeTime >= '{value}'"

    @staticmethod
    def trashed_equal(value: bool) -> str:
        return f"trashed={str(value).lower()}"

    @staticmethod
    def trashed_not_equal(value: bool) -> str:
        return f"trashed!={str(value).lower()}"

    @staticmethod
    def starred_equal(value: bool) -> str:
        return f"starred={str(value).lower()}"

    @staticmethod
    def starred_not_equal(value: bool) -> str:
        return f"starred!={str(value).lower()}"

    @staticmethod
    def folder_id(value: str) -> str:
        return f"'{value}' in parents"

    @staticmethod
    def parent_id(value: str) -> str:
        return f"'{value}' in parents"
    @staticmethod
    def owner_email(value: str) -> str:
        return f"'{value}' in owners"

    @staticmethod
    def writer_email(value: str) -> str:
        return f"'{value}' in writers"

    @staticmethod
    def reader_email(value: str) -> str:
        return f"'{value}' in readers"

    @staticmethod
    def sharedWithMe_equal(value: bool) -> str:
        return f"sharedWithMe={str(value).lower()}"

    @staticmethod
    def sharedWithMe_not_equal(value: bool) -> str:
        return f"sharedWithMe!={str(value).lower()}"

    @staticmethod
    def createdTime_less_than(value: str) -> str:
        return f"createdTime < '{value}'"

    @staticmethod
    def createdTime_less_equal(value: str) -> str:
        return f"createdTime <= '{value}'"

    @staticmethod
    def createdTime_equal(value: str) -> str:
        return f"createdTime = '{value}'"

    @staticmethod
    def createdTime_not_equal(value: str) -> str:
        return f"createdTime != '{value}'"

    @staticmethod
    def createdTime_greater_than(value: str) -> str:
        return f"createdTime > '{value}'"

    @staticmethod
    def createdTime_greater_equal(value: str) -> str:
        return f"createdTime >= '{value}'"

    @staticmethod
    def properties_has(value: str) -> str:
        return f"properties has '{value}'"

    @staticmethod
    def appProperties_has(value: str) -> str:
        return f"appProperties has '{value}'"

    @staticmethod
    def visibility_equal(value: str) -> str:
        '''
        :param value: anyoneCanFind, anyoneWithLink, domainCanFind, domainWithLink, limited
        '''
        return f"visibility = '{value}'"

    @staticmethod
    def visibility_not_equal(value: str) -> str:
        '''
        :param value: anyoneCanFind, anyoneWithLink, domainCanFind, domainWithLink, limited
        '''
        return f"visibility != '{value}'"

    @staticmethod
    def shortcutDetails_targetId_equal(value: str) -> str:
        return f"shortcutDetails.targetId = '{value}'"

    @staticmethod
    def shortcutDetails_targetId_not_equal(value: str) -> str:
        return f"shortcutDetails.targetId != '{value}'"