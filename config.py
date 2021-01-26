try:
    import sys

    print('System Version: {}'.format(sys.version))

    import os
    import requests
    import json

    from typing import Optional
    from utils import yaml_loader, BASE_DIR, listdict_to_dictdict
    from data.dhandler import csv_to_set

except ModuleNotFoundError as err:
    print('Some modules are missing: {}'.format(err))
    sys.exit()

# loaded config
config = yaml_loader(filepath=os.path.join(BASE_DIR, 'config.yml'))


class Config:
    def __init__(self):
        self._config = config  # set it to config

    def get_property(self, *property_names):

        if property_names[0] not in self._config.keys():  # we don't want KeyError
            return None  # just return None if not found

        else:
            conf_property = self._config[property_names[0]]
            for _ in property_names[1:]:
                if _ not in conf_property:
                    return None
                else:
                    conf_property = conf_property[_]

        return conf_property


class DataPathConfig(Config):
    def __init__(self):
        super().__init__()

    @property
    def stock(self) -> str:
        return str(self.get_property('data_path', 'data.stock'))

    @property
    def vocab(self) -> str:
        return str(self.get_property('data_path', 'data.vocab'))


class AppConfig(Config):
    def __init__(self):
        super().__init__()

    def browser_agent(self) -> str:
        return str(self.get_property('app', 'browser_agent'))


class YoutubeConfig(Config):
    def __init__(self):
        super().__init__()

    @property
    def days_ago(self) -> int:
        return int(self.get_property('social', 'youtube', 'days_ago'))

    @property
    def videos_per_day(self) -> int:
        return int(self.get_property('social', 'youtube', 'videos_per_day'))

    @property
    def minimum_channel_videos(self) -> int:
        return int(self.get_property('social', 'youtube', 'minimum_video_uploads_per_channel'))

    @property
    def comments_limit(self) -> int:
        return self.get_property('social', 'youtube', 'comments_limit_to_pull_per_video')

    @property
    def comment_sleep(self) -> float:
        return float(self.get_property('social', 'youtube', 'comment_loading_sleep_time'))

    @property
    def ajax_retries(self) -> int:
        return int(self.get_property('social', 'youtube', 'ajax_request_retries'))

    @property
    def ajax_sleep(self) -> float:
        return float(self.get_property('social', 'youtube', 'ajax_request_sleep_time'))


class StockConfig(Config):

    def __init__(self, exchange_id):
        super().__init__()
        self.exchange_id = str(exchange_id).upper()

    @property
    def url(self) -> str:
        return self.get_property('finance', 'stock', self.exchange_id, 'url')

    @property
    def tickers(self) -> Optional[dict]:

        try:
            response = requests.get(self.url)
            json_data = json.loads(response.text)
            list_tickers = json_data['data']
            dict_tickers = listdict_to_dictdict(dict_list=list_tickers, value_to_key='symbol')
            return dict_tickers

        except requests.exceptions.RequestException as err:
            raise SystemExit(err)


class VocabularyConfig(Config):
    def __init__(self):
        super().__init__()

    @property
    def dollar_countries(self):
        return set(self.get_property('vocabulary', 'dollar_countries'))

    @property
    def non_tickers(self):
        filepath = self.get_property('vocabulary', 'non_tickers', 'filepath')
        return csv_to_set(filepath=filepath, has_header=False)

    @property
    def stock_keywords(self):
        filepath = self.get_property('vocabulary', 'stock_keywords', 'filepath')
        return csv_to_set(filepath=filepath, has_header=False)


if __name__ == '__main__':
    ytc = YoutubeConfig()
    print(ytc.ajax_sleep)

    ac = AppConfig()
    print(ac.browser_agent())
    pass
