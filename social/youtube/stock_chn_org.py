from pyyoutube import PyYouTubeException

from config import FinanceConfig, YoutubeConfig
from mlearning.sm_processor import StockMessageProcessor
from social.youtube.youtube import Youtube

from utils import get_backdate_timestamp, zdatetime_to_timestamp, timestamp_to_zdatetime

# get stock vocabulary to check if Youtube channel is stock related
fc = FinanceConfig()
stock_vocab = fc.vocabulary

# get scanning period to see which videos have publishedAt within the given
ytc = YoutubeConfig()
backdate_scan_period = int(ytc.days_ago)
backdate_timestamp = get_backdate_timestamp(days=backdate_scan_period)
backdate_string = timestamp_to_zdatetime(backdate_timestamp)
minimum_video_uploads = int(ytc.minimum_channel_videos)


class StockChannel(Youtube):

    def __init__(self, channel_id):
        # primary channel basic info
        super().__init__()
        self.channel_id = channel_id
        self.title = str()
        self.url = 'https://www.youtube.com/channel/{channel_id}'.format(channel_id=channel_id)
        self.published_at = int()
        self.country = str()
        # to be tokenized for stock-related topic check
        self.description = str()
        self.keywords = str()

        # channel ranking assessment stats
        self.view_count = int()
        self.subscriber_count = int()
        self.video_count = int()

        # secondary channels to scrape forwards
        self.qualified_subs = set()

        # channel videos to check targeting stock:
        # TODO: scan to see which videos have publishedAt within the targeting period
        # TODO: get videos' titles and descriptions -> check stock-related and recommended tickers
        self.uploads_playlist_id = str()
        self.videos = dict()

        # channel tokens to check if stock related
        self.c_tokens = set()
        self.stock_related = bool()
        self.c_tickers = set()

    def get_channel_info(self):
        channel_info = self.get_channel(channel_id=self.channel_id)
        channel = channel_info.items[0]

        self.title = channel.snippet.title
        self.description = channel.snippet.description
        self.published_at = channel.snippet.publishedAt
        self.country = channel.snippet.country
        self.view_count = channel.statistics.viewCount
        self.subscriber_count = channel.statistics.subscriberCount
        self.video_count = channel.statistics.videoCount
        self.keywords = channel.brandingSettings.channel.keywords

        self.uploads_playlist_id = channel_info.items[0].contentDetails.relatedPlaylists.uploads

        c_text = '{description} {keywords}'.format(description=self.description, keywords=self.keywords)
        nlp = StockMessageProcessor(message=c_text)
        self.c_tokens.update(nlp.get_tickers_and_tokens()['tokens'])

    def get_videos(self):
        # channel_sections = self.get_sections(channel_id=self.channel_id)

        print('Channel ID: {}'.format(self.channel_id))
        print('Channel Title: {}'.format(self.title))

        uploads_playlist_info = self.get_playlist(playlist_id=self.uploads_playlist_id)
        if uploads_playlist_info.items:
            num_of_videos_of_upload_playlist = uploads_playlist_info.items[0].contentDetails.itemCount
            title_of_upload_playlist = uploads_playlist_info.items[0].snippet.title

            uploads_videos = self.get_playlist_videos(playlist_id=self.uploads_playlist_id)
            print('The playlist "{}" (id: {}) has {} videos'.format(title_of_upload_playlist, self.uploads_playlist_id,
                                                                    num_of_videos_of_upload_playlist))
            videos = uploads_videos.items

            for video in videos:
                video_timestamp = zdatetime_to_timestamp(video.snippet.publishedAt)
                if video_timestamp > backdate_timestamp:
                    self.videos[video.snippet.resourceId.videoId] = {
                        'publishedAt': video.snippet.publishedAt,
                        'title': video.snippet.title,
                        'description': video.snippet.description
                    }

    def get_qualified_subs(self):
        try:
            channel_subscriptions = self.get_subscriptions(channel_id=self.channel_id)
            if channel_subscriptions:
                for subscription in channel_subscriptions.items:
                    if int(subscription.contentDetails.totalItemCount) > minimum_video_uploads:
                        subscription_description = subscription.snippet.description
                        subscription_title = subscription.snippet.title
                        sub_c_text = '{description} {title}'.format(description=subscription_description,
                                                                    title=subscription_title)
                        sub_nlp = StockMessageProcessor(message=sub_c_text)
                        sub_tokens = set(sub_nlp.get_tickers_and_tokens()['tokens'])
                        if len(stock_vocab.intersection(sub_tokens)) > 0 or len(sub_tokens) == 0:
                            print('Sub Tokens Length: {}'.format(len(sub_tokens)))
                            print('Valid token: {}'.format(stock_vocab.intersection(sub_tokens)))
                            self.qualified_subs.add(subscription.snippet.resourceId.channelId)
                            # print(subscription.snippet.resourceId.channelId)
                            # print(subscription.snippet.title)

        except PyYouTubeException as err:
            print(err)

            return self.qualified_subs

    def check_stock_topic(self):
        c_text = '{description} {keywords} {title}'.format(description=self.description, keywords=self.keywords,
                                                           title=self.title)

        for video in self.videos.values():
            c_text += f" {video['title']}"
            c_text += f" {video['description']}"

        nlp = StockMessageProcessor(message=c_text)
        tickers_and_tokens = nlp.get_tickers_and_tokens()
        self.c_tokens = set(tickers_and_tokens['tokens'])
        self.c_tickers = tickers_and_tokens['tickers']

        if len(stock_vocab.intersection(self.c_tokens)) > 0 and len(self.c_tickers) > 0:
            print('Valid token: {}'.format(stock_vocab.intersection(self.c_tokens)))
            self.stock_related = True
        else:
            print('There is no matching stock keywords')
            self.stock_related = False

        return self.stock_related


if __name__ == '__main__':
    vc_channel_id = 'UCPa0bvFsR1mbBpk5mIPFGLA'
    nonstock_channel_01 = 'UCpBFiyPH5vWzF3xxxbA84xQ'  # Melecia At Home

    # vc_channel_id = 'UCaVWvC5VUaynUMUz6efdBeg' # zero video channel example
    # vc_channel_id = 'UCzSKsvUTiunCbAmV5sZ5nBQ'
    ytc = StockChannel(channel_id=vc_channel_id)
    ytc.get_channel_info()
    # ytc.get_videos()
    # ytc.get_qualified_subs()
    ytc.check_stock_topic()
    print(ytc.keywords)
    print(len(ytc.qualified_subs))




















    '''
    checking_subscriptions = set()
    checking_subscriptions.update(ytc.qualified_subs)

    checked_subscriptions = set()
    checked_subscriptions.add(vc_channel_id)

    channels_in_scope = list()
    channels_in_scope.append(ytc)

    while checking_subscriptions and len(checked_subscriptions) < 100:
        target = checking_subscriptions.pop()
        if target in checked_subscriptions:
            pass
        else:
            checked_subscriptions.add(target)
            checking_channel = YTChannel(channel_id=target)
            checking_channel.get_channel_info()
            checking_channel.get_videos()
            checking_channel.get_qualified_subs()

            if checking_channel.check_stock_topic():
                channels_in_scope.append(checking_channel)
                checking_subscriptions.update(checking_channel.qualified_subs)
                print('{}: {}'.format(checking_channel.title, checking_channel.url))

            print(f'Checking subscriptions #: {len(checking_subscriptions)}')
            print(f'Checked subscriptions #: {len(checked_subscriptions)}')
            print(f'Subscriptions in scope #: {len(channels_in_scope)}')

    print(
        '{} | {} | {} | {} | {} | {} | {} | {} | {}'.format('country', 'title', 'url', 'published_at',
                                                            'view_count', 'video_count', 'subscriber_count',
                                                            'qualified_subs', 'videos',
                                                            'c_tickers'))
    for each in channels_in_scope:
        print(
            '{} | {} | {} | {} | {} | {} | {} | {} | {} | {}'.format(each.country, each.title, each.url,
                                                                     each.published_at,
                                                                     each.view_count, each.view_count,
                                                                     each.subscriber_count,
                                                                     len(each.qualified_subs), len(each.videos),
                                                                     each.c_tickers))
    '''
