from pyyoutube import Api

from secrets.credentials import GoogleCredential

# get Youtube API Key to make data requests
g_cred = GoogleCredential()
api_dict = dict(g_cred.youtube_api_key)
api_keys = [value for value in api_dict.items()]
print(api_keys)


class YoutubeApiIterator(object):
    """Class to implement an iterator
    of Youtube API by switching API keys"""

    def __init__(self):
        self._api_keys = api_keys
        self._max = len(api_keys) - 1
        self.api_key_name = str()
        self.api_key_value = str()
        self._current_api_index = int()

    def __iter__(self):
        self._current_api_index = 0
        return self

    def __next__(self):
        if self._current_api_index <= self._max:
            self.api_key_name, self.api_key_value = api_keys[self._current_api_index]
            api_result = Api(api_key=self.api_key_value)
            self._current_api_index += 1
            return api_result

        else:
            raise StopIteration
