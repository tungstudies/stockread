from pyyoutube import Api

from secrets.credentials import GoogleCredential

google_cred = GoogleCredential()


class YoutubeScraper(object):
    def __init__(self):
        self.title = ""
        self.description = ""
        self.published_at = ""  # video
        self.rpcom = ""
        self.rppubat = ""  # comment
        self.rpauth = ""
        self.rplike = ""
        self.tcomment_count = ""
        self.tdislike_count = ""
        self.tfavorite_count = ""
        self.tlike_count = ""
        self.tview_count = ""
        # ----------------------------------------
        self.videos = []
        self.channel_id = "UCKyhocQPsAFKEY5REfVoseQ"
        self.subscribe_count = ""
        # ------------------------------------------
        self.response = ""


api = Api(api_key=google_cred.youtube_api_key)

chanel_id = 'UCPa0bvFsR1mbBpk5mIPFGLA'

chanel_info = api.get_channel_info(channel_id=chanel_id)
print(chanel_info.to_dict())
chanel_sections = api.get_channel_sections_by_channel(channel_id=chanel_id)

uploads_section = chanel_sections.items[1]
print(uploads_section.to_dict())
all_video_playlist_id = uploads_section.contentDetails.playlists[0]
print(all_video_playlist_id)

playlist_item_by_playlist = api.get_playlist_items(playlist_id=all_video_playlist_id, count=100)  # count=None to get all
print('--------------------------------------------------------------------')
print(len(playlist_item_by_playlist.items))
print('Video Info from playlist call UEw2djdwTGt1TUxjTktlc0FTUUh4aVJERFZGSEFRbldTci5ERkUyQTM0MzEwQjZCMTY5 UEw2djdwTGt1TUxjTktlc0FTUUh4aVJERFZGSEFRbldTci5ERkUyQTM0Mz: {}'.format(playlist_item_by_playlist.items[1].to_dict()))
print('--------------------------------------------------------------------')
video = playlist_item_by_playlist.items[1].snippet.resourceId
video_id = video.to_dict()['videoId']
# print('video id: ' + video_id)
# video_id = 'Q73NuMhE5VA'

video_by_id = api.get_video_by_id(video_id=video_id)
print('Video Info: {}'.format(video_by_id.to_dict()))


ct_by_video = api.get_comment_threads(video_id=video_id, count=None)
comment_threads = ct_by_video.items
for comment_thread in comment_threads[5:6]:
    toplevel_comment = (comment_thread.snippet.topLevelComment.snippet.authorDisplayName,
                        comment_thread.snippet.topLevelComment.snippet.textDisplay)
    print(toplevel_comment)
    reply_comments = [(x.snippet.authorDisplayName, x.snippet.textDisplay) for x in comment_thread.replies.comments]
    print(reply_comments)
    # print(comment_thread.
    # comment_thread_id = comment_thread.id
    # ct_by_id = api.get_comment_thread_by_id(comment_thread_id=comment_thread_id)
    # print(ct_by_id.to_dict())

# get subscriptions:

vincent_subscriptions = api.get_subscription_by_channel(channel_id=chanel_id, parts="id,snippet",
                                                        count=2)
chanel_first = vincent_subscriptions.items[0]
# chanel_first
chanel_first_id = chanel_first.snippet.resourceId.channelId
chanel_first_name = chanel_first.snippet.title
print('{}: https://www.youtube.com/channel/{}'.format(chanel_first_name,chanel_first_id))
print(chanel_first.to_dict())

# comment_01 = comments[1].snippet
# print(comment_01.to_dict())
# for each in items:
#     item.snippet.resourceId
#
# print(items)
