from enum import Enum

from colorama import Fore


class Permissions:
    def __init__(self, drive):
        self.drive = drive

    def add(self, file_id, role, email=None, domain=None):
        '''
        Add permission to a file|folder
        :param file_id: File|folder ID
        :param role: Use constants.Roles or visit https://developers.google.com/drive/api/guides/ref-roles
        :param email: Email address
        :param domain: Domain, e.g. google.com
        :return: Permission info
        '''
        provided_args = [email, domain]
        provided_count = sum(arg is not None for arg in provided_args)
        if provided_count != 1:
            raise ValueError("Please provide exactly one of email or domain")

        if isinstance(role, Enum):
            role_value = role.value
            role_name = role.name.capitalize()
        else:
            role_value = role.lower()
            role_name = role.capitalize()

        if email:
            body = {"type": "user", "role": role_value, "emailAddress": email}
        elif domain:
            body = {"type": "domain", "role": role_value, "domain": domain}

        result = self.drive.service.permissions().create(fileId=file_id, body=body, fields="*").execute()

        self.drive.print_if_verbose(
            f"{Fore.GREEN}Added {Fore.RESET}{role_name} {Fore.GREEN}permission for {Fore.RESET}{email or domain} {Fore.GREEN}to {Fore.RESET}{file_id}")
        return result

    def transfer_ownership(self, file_id, email):
        '''
        Transfer ownership of a file|folder to an email
        :param file_id: File|folder ID
        :param email: Email address
        :return: Ownership info
        '''
        body = {'type': 'user', 'role': 'owner', 'emailAddress': email}
        result = self.drive.service.permissions().create(fileId=file_id, body=body, transferOwnership=True,
                                                         fields='*').execute()

        self.drive.print_if_verbose(
            f"{Fore.BLUE}Transferred ownership of {Fore.RESET}{file_id} {Fore.BLUE}to {Fore.RESET}{email}")

        return result

    def get(self, file_id, permission_id=None, email=None, domain=None):
        '''
        Get permission info
        :param file_id: File|Folder ID
        :param permission_id: Permission ID
        :return:
        '''
        provided_args = [permission_id, email, domain]
        provided_count = sum(arg is not None for arg in provided_args)
        if provided_count != 1:
            raise ValueError("Please provide exactly one of permission_id, email, or domain")

        if permission_id:
            return self.drive.service.permissions().get(fileId=file_id, permissionId=permission_id,
                                                        fields='*').execute()
        elif email or domain:
            permissions = self.list(file_id=file_id)

            if email:
                permission = [p for p in permissions if p.get('emailAddress') == email]
            elif domain:
                permission = [p for p in permissions if p.get('domain') == domain]

            if permission:
                return permission[0]
            else:
                raise ValueError(f"Permission not found: {email or domain}")

    def update(self, file_id, role, permission_id=None, email=None, domain=None):
        provided_args = [permission_id, email, domain]
        provided_count = sum(arg is not None for arg in provided_args)
        if provided_count != 1:
            raise ValueError("Please provide exactly one of permission_id, email, or domain")

        if isinstance(role, Enum):
            role_value = role.value
            role_name = role.name.capitalize()
        else:
            role_value = role.lower()
            role_name = role.capitalize()

        body = {'role': role_value}

        if permission_id:
            pass
        elif email or domain:
            permissions = self.list(file_id=file_id)

            if email:
                permission = [p for p in permissions if p.get('emailAddress') == email]
            elif domain:
                permission = [p for p in permissions if p.get('domain') == domain]

            if permission:
                permission_id = permission[0]['id']
            else:
                raise ValueError(f"Permission not found: {email or domain}")

        result = self.drive.service.permissions().update(fileId=file_id, permissionId=permission_id, body=body,
                                                         fields='*').execute()

        self.drive.print_if_verbose(
            f"{Fore.BLUE}Updated permission of {Fore.RESET}{email or domain or permission_id}{Fore.BLUE} in file {Fore.RESET}{file_id}{Fore.BLUE} to {Fore.RESET}{role_name}")

        return result

    def list(self, file_id):
        '''
        Get a list of permissions of a file|folder
        :param file_id: File|folder ID
        :return: Permission info
        '''
        return self.drive.service.permissions().list(fileId=file_id, fields='permissions').execute()['permissions']

    def remove(self, file_id, permission_id=None, email=None, domain=None):
        '''
        Remove a permission from a file|folder
        :param file_id: File|folder ID
        :param email: Email address
        :param permission_id: Permission ID
        '''
        provided_args = [permission_id, email, domain]
        provided_count = sum(arg is not None for arg in provided_args)
        if provided_count != 1:
            raise ValueError("Please provide exactly one of permission_id, email, or domain")

        if permission_id:
            pass
        elif email or domain:
            permissions = self.list(file_id=file_id)

            if email:
                permission = [p for p in permissions if p.get('emailAddress') == email]
            elif domain:
                permission = [p for p in permissions if p.get('domain') == domain]

            if permission:
                permission_id = permission[0]['id']
            else:
                raise ValueError(f"Permission not found: {email or domain}")

        self.drive.service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
        self.drive.print_if_verbose(
            f"{Fore.RED}Removed permission of {Fore.RESET}{email or domain or permission_id} {Fore.RED}from {Fore.RESET}{file_id}")
