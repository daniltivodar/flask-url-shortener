from datetime import datetime as dt

from flask import url_for

from yacut import db


class URLMap(db.Model):
    """Модель сохранения ссылок и их коротких версий."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16))
    timestamp = db.Column(db.DateTime, index=True, default=dt.now())

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'short_redirect_view',
                short_link=self.short,
                _external=True,
            ),
        )

    def from_dict(self, data):
        for key, value in zip(('original', 'short'), ('url', 'custom_id')):
            setattr(self, key, data[value])
