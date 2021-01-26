from dataclasses import dataclass

from social.youtube.youtube_chn import Channel


@dataclass
class StockChannel(Channel):
    def __init__(self, channel_id):
        super().__init__(channel_id)




if __name__ == '__main__':
    sc = StockChannel(channel_id='UCUvvj5lwue7PspotMDjk5UA')
    print(sc.total_views)