from pyyoutube.models.base import BaseModel

try:
    import sys

    print('System Version: {}'.format(sys.version))

    import requests

    from dataclasses import dataclass, field
    from typing import Optional

    from config import YoutubeConfig

except ModuleNotFoundError as err:
    print('Some modules are missing: {}'.format(err))
    sys.exit()


@dataclass
class Comment(BaseModel):
    """
    A class representing for Youtube comment.

    """
    comment_id: Optional[str] = field(default=None, repr=False)
    text: Optional[str] = field(default=None, repr=False)
    time: Optional[str] = field(default=None,repr=False)
    author: Optional[str] = field(default=None, repr=False)
    author_channel: Optional[str] = field(default=None, repr=False)
    votes: Optional[int] = field(default=0, repr=False)


