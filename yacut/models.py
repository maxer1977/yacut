import re
from datetime import datetime
from random import choice

from flask import url_for

from . import db
from .constants import LINK_LEN, MATCH_SHORT_LINK, STRING_FOR_LINK


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # метод для формирования json-словаря
    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for("link_view", short=self.short, _external=True),
        )

    # метод для автоформирования короткого имени
    def get_unique_short_id(self):
        auto_link = "".join(choice(STRING_FOR_LINK) for _ in range(LINK_LEN))
        return auto_link

    # метод проверки предоставленного короткого имени
    def check_link(self, link):
        pattern = MATCH_SHORT_LINK
        return re.match(pattern, link)
