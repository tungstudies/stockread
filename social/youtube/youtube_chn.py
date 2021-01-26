try:
    import sys

    import re
    import shlex  # to split text respecting quotes
    import requests

    from dataclasses import dataclass, field
    from typing import Optional

    import xml.etree.ElementTree as ElementTree  # to sparse xml response
    from pyyoutube.models.base import BaseModel

    from utils import kmb_to_number, time_ago

except ModuleNotFoundError as err:
    print('Some modules are missing: {}'.format(err))
    sys.exit()


@dataclass
class Channel(BaseModel):
    """
    A class representing for Youtube channel.

    """

    channel_id: Optional[str] = field(default=None, repr=True)
    channel_name: Optional[str] = field(default=None, repr=True)
    url: Optional[str] = field(default=None, repr=False)
    country: Optional[str] = field(default=None, repr=False)
    joining_date: Optional[str] = field(default=None, repr=False)
    total_views: Optional[int] = field(default=0, repr=False)
    total_subscribers: Optional[int] = field(default=0, repr=False)
    latest_video_url: Optional[str] = field(default=None, repr=False)
    latest_video_title: Optional[str] = field(default=None, repr=False)
    latest_video_date: Optional[str] = field(default=None, repr=False)
    latest_video_time_ago: Optional[int] = field(default=None, repr=False)
    keywords: Optional[str] = field(default=None, repr=False)

    def __post_init__(self):

        self.url: Optional[str] = f'https://www.youtube.com/channel/{self.channel_id}'
        self.feeds_url: Optional[str] = f'https://www.youtube.com/feeds/videos.xml?channel_id={self.channel_id}'

        self._about_page_content: Optional[str] = self._go_to_about_page()
        self._feeds_xml_data: Optional[str] = self._get_feeds_xml()

        self.channel_name = self.get_channel_name()
        self.country = self.get_country()
        self.joining_date = self.get_joining_date()
        self.description = self.get_description()
        self.total_views = self.get_total_views()
        self.total_subscribers = self.get_subscribers()
        self.keywords = self.get_keywords().__repr__()
        self.videos = self.get_feeds()
        self.latest_video_url = f"https://www.youtube.com/watch?v={self.videos[0]['id']}"
        self.latest_video_title = self.videos[0]['title']
        self.latest_video_date = self.videos[0]['published']
        self.latest_video_time_ago = time_ago(self.latest_video_date)

    def _go_to_about_page(self):
        response = requests.get(f'https://www.youtube.com/channel/{self.channel_id}/about')
        return response.text

    def _go_to_channels_page(self):
        response = requests.get(f'https://www.youtube.com/channel/{self.channel_id}/about')
        return response.text

    def _get_feeds_xml(self):
        response = requests.get(self.feeds_url)
        if response.encoding == 'UTF-8':
            xml_data = str(response.text).replace('\n', '')
        else:
            xml_data = str(response.content).replace('\n', '')

        return xml_data

    def get_channel_name(self) -> str:
        pattern = re.compile(r'", "name": "(.*?)"}}]}')
        return pattern.findall(self._about_page_content)[0]

    def get_joining_date(self) -> str:
        pattern = re.compile(r' "},{"text":"(.*?)"}]},"canonicalChannelUrl"')
        return pattern.findall(self._about_page_content)[0]

    def get_description(self) -> str:
        pattern = re.compile(r'MetadataRenderer":{"description":{"simpleText":"(.*?)"}')
        return pattern.findall(self._about_page_content)[0]

    def get_total_views(self) -> int:
        pattern = re.compile(r'"viewCountText":{"simpleText":"(.*?) views"},"joinedDateText"')
        total_view_str = pattern.findall(self._about_page_content)[0]
        total_view_int = int(str(total_view_str).replace(',', ''))
        return total_view_int

    def get_subscribers(self) -> int:
        pattern = re.compile(r'"subscriberCountText":{"simpleText":"(.*?) subscribers"},"tvBanner"')
        sub_count_str = pattern.findall(self._about_page_content)[0]
        sub_count_int = kmb_to_number(sub_count_str)
        return sub_count_int

    def get_country(self) -> str:
        pattern = re.compile(r'country":{"simpleText":"(.*?)"},"showDescription')
        return pattern.findall(self._about_page_content)[0]

    def get_keywords(self) -> list:
        pattern = re.compile(r'","keywords":"(.*?)","ownerUrls":')
        keyword_str = pattern.findall(self._about_page_content)[0]
        # to split text respecting quotes
        keyword_list = shlex.split(str(keyword_str).replace('\\', ''))
        return keyword_list

    def get_feeds(self) -> list:

        root = ElementTree.fromstring(self._feeds_xml_data)

        ns = '{http://www.w3.org/2005/Atom}'
        yt_ns = '{http://www.youtube.com/xml/schemas/2015}'
        media_ns = '{http://search.yahoo.com/mrss/}'

        videos = list()
        for entry in root.findall(ns + "entry"):
            # empty news dictionary
            entry_data = {
                'id': entry.find(yt_ns + 'videoId').text,
                'title': entry.find(media_ns + "group").find(media_ns + 'title').text,
                'description': entry.find(media_ns + "group").find(media_ns + 'description').text,
                'published': entry.find(ns + 'published').text,

                'view_count': entry.find(media_ns + "group").find(media_ns + 'community').find(media_ns + 'statistics')
                    .attrib.get('views'),

                'like_count': entry.find(media_ns + "group").find(media_ns + 'community').find(media_ns + 'starRating')
                    .attrib.get('count'),

                'avg_rating': entry.find(media_ns + "group").find(media_ns + 'community').find(media_ns + 'starRating')
                    .attrib.get('average'),
            }
            videos.append(entry_data)

        return videos


if __name__ == '__main__':
    pass
