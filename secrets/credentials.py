import os

from utils import yaml_loader, BASE_DIR

# loaded credentials
cred = yaml_loader(filepath=os.path.join(BASE_DIR, 'secrets', 'credentials.yml'))


class Credential(object):
    def __init__(self):
        self._cred = cred  # set it to cred

    def get_credential(self, *cred_keys):
        cred_val = self._cred
        for _ in cred_keys:
            if _ not in cred_val:
                return None
            else:
                cred_val = cred_val[_]
        return cred_val


class GoogleCredential(Credential):
    @property
    def youtube_api_key(self) -> str:
        return self.get_credential('google', 'youtube', 'api_key')

    @property
    def sheets_account_service_jsonpath(self) -> str:
        return self.get_credential('google', 'sheets', 'service_account_filepath')


class AVCredential(Credential):
    @property
    def api_key(self) -> str:
        return self.get_credential('alpha_vantage', 'api_key')


if __name__ == '__main__':
    g_cred = GoogleCredential()
    print(g_cred.sheets_account_service_jsonpath)
    # api_keys = [value for value in api_dict.values()]
    # print(api_keys)
    pass
