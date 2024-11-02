from enum import Enum

from colorama import Fore


class Permissions:
    def __init__(self, drive):
        self.drive = drive
        self.email_address = None

    def add(self, file_id, role, email=None, domain=None, anyone=False):
        '''
        Add permission to a file or folder. Please provide exactly one of email or domain.
        :param file_id: File | folder ID.
        :param role: Use Roles or visit https://developers.google.com/drive/api/guides/ref-roles.
        :param email: Email address.
        :param domain: Domain, e.g. google.com.
        :param anyone: Anyone with link.
        :return: Permission info.
        '''


        provided_args = [email, domain, anyone]
        provided_count = sum([1 for arg in provided_args if arg is not None and arg is not False])
        if provided_count != 1:
            raise ValueError("Please provide exactly one of email, domain or anyone.")

        if isinstance(role, Enum):
            role_value = role.value
            role_name = role.name.capitalize()
        else:
            role_value = role.lower()
            role_name = role.capitalize()

        if anyone:
            body = {"type": "anyone", "role": role_value}
        elif email:
            body = {"type": "user", "role": role_value, "emailAddress": email}
        elif domain:
            body = {"type": "domain", "role": role_value, "domain": domain}

        result = self.drive.service.permissions().create(fileId=file_id, body=body, fields="*").execute()

        self.drive.print_if_verbose(
            f"{Fore.GREEN}Added {Fore.RESET}{role_name} {Fore.GREEN}permission for {Fore.RESET}{email or domain} {Fore.GREEN}to {Fore.RESET}{file_id}")
        return result

    def transfer_ownership(self, file_id, email):
        '''
        Transfer ownership of a file or folder to an email.
        :param file_id: File | folder ID.
        :param email: Email address.
        :return: Ownership info.
        '''

        email = email.lower().strip()

        if not self.email_address:
            about = self.drive.service.about().get(fields='*').execute()
            self.email_address = about['user']['emailAddress']

        current_domain = self.email_address.split('@')[-1]
        new_domain = email.split('@')[-1]

        if current_domain != new_domain:
            raise PermissionError(f"{email} is not in your organization ({current_domain}).")

        if '@gmail.' not in email:
            body = {'type': 'user', 'role': 'owner', 'emailAddress': email}
            result = self.drive.service.permissions().create(fileId=file_id, body=body, transferOwnership=True, fields='*').execute()
        else:
            # https://stackoverflow.com/questions/78308635/unable-to-transfer-ownership-in-google-drive-v3-api-in-my-node-project
            permission = self.add(file_id=file_id, email=email, role='writer')
            body = {'role': 'writer', 'pendingOwner': True}
            result = self.drive.service.permissions().update(fileId=file_id, permissionId=permission['id'], body=body, fields='*').execute()

        self.drive.print_if_verbose(f"{Fore.BLUE}Transferred ownership of {Fore.RESET}{file_id} {Fore.BLUE}to {Fore.RESET}{email}")

        return result

    def get(self, file_id, permission_id=None, email=None, domain=None, anyone=False):
        '''
        Get permission info. Please provide exactly one of permission_id, email, or domain.
        :param file_id: File | Folder ID.
        :param permission_id: Permission ID.
        :param email: Email address.
        :param domain: Domain, e.g. google.com.
        :param anyone: Anyone with link.
        :return: Permission info.
        '''
        provided_args = [permission_id, email, domain, anyone]
        provided_count = sum([1 for arg in provided_args if arg is not None and arg is not False])
        if provided_count != 1:
            raise ValueError("Please provide exactly one of permission_id, email, domain or anyone.")


        if anyone:
            permission_id = 'anyoneWithLink'

        if permission_id:
            return self.drive.service.permissions().get(fileId=file_id, permissionId=permission_id, fields='*').execute()

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

    def update(self, file_id, role, permission_id=None, email=None, domain=None, anyone=False):
        '''
        Update a permission. Please provide exactly one of permission_id, email, or domain.
        :param file_id: File ID.
        :param role: Use Roles or visit https://developers.google.com/drive/api/guides/ref-roles.
        :param permission_id: Permission ID.
        :param email: Email address.
        :param domain: Domain, e.g. google.com.
        :param anyone: Anyone with link.
        :return: Permission info.
        '''
        provided_args = [permission_id, email, domain, anyone]
        provided_count = sum([1 for arg in provided_args if arg is not None and arg is not False])
        if provided_count != 1:
            raise ValueError("Please provide exactly one of permission_id, email, domain, or anyone")

        if isinstance(role, Enum):
            role_value = role.value
            role_name = role.name.capitalize()
        else:
            role_value = role.lower()
            role_name = role.capitalize()

        body = {'role': role_value}

        if permission_id:
            pass
        elif anyone:
            permission_id = 'anyoneWithLink'
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

        self.drive.print_if_verbose(f"{Fore.BLUE}Updated {Fore.RESET}{email or domain or permission_id}{Fore.BLUE}'s permission in file {Fore.RESET}{file_id}{Fore.BLUE} to {Fore.RESET}{role_name}")

        return result

    def list(self, file_id):
        '''
        Get a list of permissions of a file or folder.
        :param file_id: File | folder ID.
        :return: Permission info.
        '''
        return self.drive.service.permissions().list(fileId=file_id, fields='permissions').execute()['permissions']

    def remove(self, file_id, permission_id=None, email=None, domain=None, anyone=False):
        '''
        Remove a permission from a file | folder. Please provide exactly one of permission_id, email, or domain.
        :param file_id: File | folder ID.
        :param permission_id: Permission ID.
        :param email: Email address.
        :param domain: Domain, e.g. google.com.
        :param anyone: Anyone with link.
        '''
        provided_args = [permission_id, email, domain, anyone]
        provided_count = sum([1 for arg in provided_args if arg is not None and arg is not False])
        if provided_count != 1:
            raise ValueError("Please provide exactly one of permission_id, email, domain, or anyone.")

        if permission_id:
            pass
        elif anyone:
            permission_id = 'anyoneWithLink'
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
        self.drive.print_if_verbose(f"{Fore.RED}Removed {Fore.RESET}{email or domain or permission_id}{Fore.RED}'s permission from {Fore.RESET}{file_id}")