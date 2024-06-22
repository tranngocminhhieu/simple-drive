from colorama import Fore

class About:
    def __init__(self, drive):
        self.drive = drive


    def get(self, fields="*"):
        '''
        Get the account info.
        :param fields: A list of fields, defaults to "*".
        :return: Account info.
        '''
        if isinstance(fields, list):
            fields = ', '.join(fields)
        return self.drive.service.about().get(fields=fields).execute()

    def get_storage_quota(self):
        '''
        Get the account storage quota.
        :return: Storage quota info.
        '''
        quota = self.drive.service.about().get(fields="storageQuota").execute()['storageQuota']

        for key in quota:
            quota[key] = int(quota[key])

        try:
            limit = round(quota['limit'] / 1024 / 1024 / 1024, 2)
            usage = round(quota['usage'] / 1024 / 1024 / 1024, 2)
            usage_percent = round(usage / limit * 100, 2)
            if usage_percent < 30:
                color = Fore.GREEN
            elif usage_percent < 70:
                color = Fore.YELLOW
            else:
                color = Fore.RED
            self.drive.print_if_verbose(f"{color}{usage:0,.2f} GB{Fore.RESET} / {limit:0,.2f} GB (usage {usage_percent}%)")
        except:
            pass

        return quota