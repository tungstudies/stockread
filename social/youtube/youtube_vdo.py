from pyyoutube.models.base import BaseModel

try:
    import sys

    print('System Version: {}'.format(sys.version))

    import re
    import requests
    import time

    import lxml.html
    from typing import Optional
    from dataclasses import field, dataclass
    from lxml.cssselect import CSSSelector

    from config import YoutubeConfig, AppConfig
    from social.youtube.youtube_cmt import Comment


except ModuleNotFoundError as err:
    print('Some modules are missing: {}'.format(err))
    sys.exit()

ytc = YoutubeConfig()
COMMENTS_LIMIT = ytc.comments_limit
COMMENT_SLEEP = ytc.comment_sleep
AJAX_SLEEP = ytc.ajax_sleep
AJAX_RETRIES = ytc.ajax_retries

app_conf = AppConfig()
BROWSER_AGENT = app_conf.browser_agent()

YOUTUBE_COMMENTS_AJAX_OLD_API_URL = 'https://www.youtube.com/comment_ajax'
YOUTUBE_COMMENTS_AJAX_NEW_API_URL = 'https://www.youtube.com/comment_service_ajax'


@dataclass
class Video(BaseModel):
    """
    A class representing for Youtube video.

    """

    video_id: Optional[str] = field(default=None, repr=True)
    comments_limit: Optional[int] = field(default=COMMENTS_LIMIT, repr=False)

    def __post_init__(self):
        self.url: Optional[str] = f'https://www.youtube.com/watch?v={self.video_id}'

        self.session = requests.Session()
        self.session.headers['User-Agent'] = BROWSER_AGENT
        self.video_html: Optional[str] = self._go_to_page()

        if r'"isLiveContent":true' in self.video_html:
            print('Livestream video detected! Not all comments may be downloaded.')
            self.is_livestream: Optional[bool] = True
        else:
            self.is_livestream: Optional[bool] = False

        self.comment_count: int = 0
        self.comments = list()

    def get_video_comments(self):
        if self.is_livestream:
            # Use the new youtube API to download all comments (does not work for recorded videos)
            return self._get_livestream_comments()
        else:
            # Use the old youtube API to download all comments (does not work for live streams)
            return self._get_recorded_video_comments()

    def _go_to_page(self):
        # Get Youtube page with initial comments if exists (often time, first request does not have comments)
        response = self.session.get(self.url)
        return response.text

    def _get_livestream_comments(self):
        # TODO: Finish implementing livestreams' comments
        pass

    def _get_recorded_video_comments(self):
        # Extract reply comment ids of the initial response html
        text_html = self.video_html
        tree = lxml.html.fromstring(text_html)
        ssc_select = CSSSelector('.comment-replies-header > .load-comments')
        reply_cids = [i.get('data-cid') for i in ssc_select(tree)]

        # Add comment_ids to list of all comment ids to crawl one by one
        ret_cids = list()
        for comment in self.__extract_comments(text_html):
            ret_cids.append(comment.comment_id)
            # yield comment
            self.comments.append(comment)
            self.comment_count += 1

        page_token = self.__find_value(html_text=text_html, key='data-token')
        session_token = self.__find_value(html_text=text_html, key='XSRF_TOKEN', num_chars=3)
        session_token = bytes(session_token, 'ascii').decode('unicode-escape')

        first_iteration = True

        # Get remaining comments (the same as performing scrolling down the video page to see more comments)

        while page_token:
            data = {'video_id': self.video_id,
                    'session_token': session_token}

            params = {'action_load_comments': 1,
                      'order_by_time': True,
                      'filter': self.video_id}

            if first_iteration:
                params['order_menu'] = True
            else:
                data['page_token'] = page_token

            # make ajax request to get more comments loaded
            response = self.__ajax_request(self.session, YOUTUBE_COMMENTS_AJAX_OLD_API_URL, params, data)
            if not response:
                break

            # retrieving new page token after the ajax request
            # regenerate html text after the ajax request
            page_token, text_html = response.get('page_token', None), response['html_content']

            reply_cids += self.__extract_reply_cids(text_html)
            for comment in self.__extract_comments(text_html):
                if comment.comment_id not in ret_cids:
                    ret_cids.append(comment.comment_id)

                    # yield comment
                    self.comments.append(comment)
                    self.comment_count += 1

            first_iteration = False
            time.sleep(COMMENT_SLEEP)

        # Get replies (the same as pressing the 'View all X replies' link)
        for cid in reply_cids:
            data = {'comment_id': cid,
                    'video_id': self.video_id,
                    'can_reply': 1,
                    'session_token': session_token}

            params = {'action_load_replies': 1,
                      'order_by_time': True,
                      'filter': self.video_id,
                      'tab': 'inbox'}

            response = self.__ajax_request(self.session, YOUTUBE_COMMENTS_AJAX_OLD_API_URL, params, data)
            if not response:
                break

            text_html = response['html_content']

            for comment in self.__extract_comments(text_html):
                if comment.comment_id not in ret_cids:
                    ret_cids.append(comment.comment_id)
                    # yield comment
                    self.comments.append(comment)
                    self.comment_count += 1

            time.sleep(COMMENT_SLEEP)

    @staticmethod
    def __extract_comments(html_text):
        tree = lxml.html.fromstring(html_text)
        item_sel = CSSSelector('.comment-item')

        # get components of item_sel
        text_sel = CSSSelector('.comment-text-content')
        time_sel = CSSSelector('.time')
        author_sel = CSSSelector('.user-name')
        vote_sel = CSSSelector('.like-count.off')

        comments = list()
        # create generators of each comment with its attributes
        for item in item_sel(tree):
            cid = item.get('data-cid')
            text = text_sel(item)[0].text_content()
            time = time_sel(item)[0].text_content().strip()
            author = author_sel(item)[0].text_content()
            channel = item[0].get('href').replace('/channel/', '').strip()
            votes = vote_sel(item)[0].text_content() if len(vote_sel(item)) > 0 else 0
            comments.append(
                Comment(comment_id=cid, text=text, author=author, time=time, author_channel=channel, votes=votes))

        return comments

    @staticmethod
    def __find_value(html_text: str, key: str, num_chars: int = 2, separator: str = '"') -> str:
        pos_begin: int = html_text.find(key) + len(key) + num_chars
        pos_end: int = html_text.find(separator, pos_begin)
        return html_text[pos_begin: pos_end]

    @staticmethod
    def __ajax_request(session, url: str, params=None, data=None, headers=None, retries=AJAX_RETRIES, sleep=AJAX_SLEEP):
        for _ in range(retries):
            response = session.post(url, params=params, data=data, headers=headers)
            if response.status_code == 200:
                return response.json()
            if response.status_code in [403, 413]:
                return {}
            else:
                time.sleep(sleep)

    @staticmethod
    def __extract_reply_cids(html_text: str) -> list:
        tree = lxml.html.fromstring(html_text)
        sel = CSSSelector('.comment-replies-header > .load-comments')
        return [i.get('data-cid') for i in sel(tree)]

    def get_title(self):
        pat = re.compile(r',"title":"(.*?)","lengt')
        return pat.findall(self.video_html)[0]

    def get_view_count(self):
        pat = re.compile(r':{"videoViewCountRenderer":{"viewCount":{"simpleText":"(.*?) views"},"shortViewCo')
        view_str = pat.findall(self.video_html)[0]
        view_int = int(str(view_str).replace(',', ''))
        return view_int

    def get_description(self):
        pat = re.compile(r'"},"description":{"simpleText":"(.*?)"},"lengthSeconds":"')
        return pat.findall(self.video_html)[0]

    def get_length_seconds(self):
        pat = re.compile(r'"},"lengthSeconds":"(.*?)","ownerProfileUrl"')
        return pat.findall(self.video_html)[0]

    def get_owner_channel_id(self):
        pat = re.compile(r'"externalChannelId":"(.*?)","isFamilySafe"')
        return pat.findall(self.video_html)[0]

    def get_publish_date(self):
        pat = re.compile(r'"publishDate":"(.*?)","ownerChan')
        return pat.findall(self.video_html)[0]

    def get_category(self):
        pat = re.compile(r'"category":"(.*?)","publishDate"')
        result = pat.findall(self.video_html)[0]
        words = str(result).split(' ')
        return " & ".join(word for word in words if word.isalpha())

    def get_like_count(self):
        pat = re.compile(r'accessibility":{"label":"like this video along with (.*?) other')
        like_count_str = pat.findall(self.video_html)[0]
        like_count_int = int(str(like_count_str).replace(',', ''))
        return like_count_int

    def get_dislike_count(self):
        pat = re.compile(r'accessibilityData":{"label":"dislike this video along with (.*?) other')
        dislike_count_str = pat.findall(self.video_html)[0]
        dislike_count_int = int(str(dislike_count_str).replace(',', ''))
        return dislike_count_int

    def get_keywords(self):
        pattern = re.compile(r'keywords":\[(.*?)],"channelId')
        keyword_str = pattern.findall(self.video_html)[0]
        # to split text respecting quotes
        keyword_list = str(keyword_str).replace('"', '').split(',')
        return keyword_list


if __name__ == '__main__':
    video_code = 'DH920207C9w'
    video = Video(video_code)
    video.get_video_comments()

    for each in video.comments:
        print(each.comment_id)

    print(len(video.comments))
