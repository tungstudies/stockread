from pyyoutube import Api

from config import YoutubeConfig
from secrets.credentials import GoogleCredential

# get Youtube API Key to make data requests

g_cred = GoogleCredential()
api_dict = dict(g_cred.youtube_api_key)
api_keys = [value for value in api_dict.values()]

api = Api(api_key=api_keys[2])

# get scanning period to compute maximum number of videos to request
ytc = YoutubeConfig()
backdate_scan_period = int(ytc.days_ago)
max_daily_uploads = int(ytc.videos_per_day)
max_video_count = backdate_scan_period * max_daily_uploads


class Youtube(object):
    def __init__(self):
        self._api = api

    def get_channel(self, channel_id):
        parts = ["id", "snippet", "contentDetails", "statistics", "brandingSettings", "topicDetails"]
        return self._api.get_channel_info(channel_id=channel_id, parts=parts)

    def get_sections(self, channel_id):
        return self._api.get_channel_sections_by_channel(channel_id=channel_id)

    def get_playlist_videos(self, playlist_id, num_of_videos=max_video_count):
        return self._api.get_playlist_items(playlist_id=playlist_id, count=num_of_videos)  # count=None to get all

    def get_video(self, video_id):
        return self._api.get_video_by_id(video_id=video_id)

    def get_comment_threads(self, video_id, comment_count=None):
        return self._api.get_comment_threads(video_id=video_id, count=comment_count)  # count=None to get all

    def get_playlist(self, playlist_id):
        return self._api.get_playlist_by_id(playlist_id=playlist_id)

    def get_subscriptions(self, channel_id, parts="id,snippet,contentDetails", subscription_count=None):
        return self._api.get_subscription_by_channel(channel_id=channel_id, parts=parts,
                                                     count=subscription_count)

    def get_videos_by_query(self, query, published_after,
                            search_type="video", parts=["id", "snippet"],
                            order="date", count=max_video_count):
        return self._api.search(q=query, published_after=published_after,
                                search_type=search_type, parts=parts, order=order, count=count)

    def get_video_category(self, category_id):
        return self._api.get_video_categories(category_id=category_id, parts='snippet')


if __name__ == '__main__':
    youtube = Youtube()
    channel_id = 'UCPa0bvFsR1mbBpk5mIPFGLA'

    video_id = "BPwUay1bsUY"
    # video_id = "dgDc3j-2RPQ"
    print(youtube.get_video(video_id).to_dict())
    # print(youtube.get_video_category(category_id="27").to_dict())
    # subscriptions = youtube.get_subscriptions(channel_id=vc_channel_id)
    # print(subscriptions.to_dict())
    # channel_id = 'UCpBFiyPH5vWzF3xxxbA84xQ'  # Melecia At Home
    # channel = youtube.get_channel(channel_id=channel_id)
    # print(channel.to_dict())

    # print(youtube.get_video_category().to_dict())
