from pyyoutube import Api, PyYouTubeException

from config import FinanceConfig, YoutubeConfig
from secrets.credentials import GoogleCredential
from mlearning.sm_processor import StockMessageProcessor

from utils import get_backdate_timestamp, zdatetime_to_timestamp

# get Youtube API Key to make data requests
g_cred = GoogleCredential()
api = Api(api_key=g_cred.youtube_api_key)

# get stock vocabulary to check if Youtube channel is stock related
fc = FinanceConfig()
stock_vocab = fc.vocabulary

# get scanning period to see which videos have publishedAt within the given
ytc = YoutubeConfig()
backdate_scan_period = int(ytc.days_ago)
max_daily_uploads = int(ytc.videos_per_day)
num_of_videos = backdate_scan_period * max_daily_uploads
backdate_timestamp = get_backdate_timestamp(days=backdate_scan_period)

# class YoutubeVideo(object)
