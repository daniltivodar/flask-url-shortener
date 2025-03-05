from datetime import datetime as dt
from random import sample
import re

from flask import url_for

from settings import (
    ACCEPTABLE_SYMBOLS,
    LINK_LENGTH,
    MAX_LENGTH_ORIGINAL_URL,
    MAX_LENGTH_SHORT_URL,
    R_STRING,
    SHORT_REDIRECT_VIEW,
)
from yacut import db
from yacut.error_handlers import ObjectCreationException

MAX_LENGTH_ERROR_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
UNIQUE_ERROR_MESSAGE = 'Предложенный вариант короткой ссылки уже существует.'
WRONG_NAME_ERROR_MESSAGE = 'Указано недопустимое имя для короткой ссылки'


class URLMap(db.Model):
    """Модель сохранения ссылок и их коротких версий."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL_URL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT_URL))
    timestamp = db.Column(db.DateTime, index=True, default=dt.now)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                SHORT_REDIRECT_VIEW,
                short=self.short,
                _external=True,
            ),
        )

    def get_short_redirect_url(self):
        return url_for(
            SHORT_REDIRECT_VIEW,
            short=self.short,
            _external=True,
        )

    @classmethod
    def check_uniqueness_short(cls, short):
        """Проверяет уникальность короткой ссылки."""
        return cls.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short():
        """Метод создания случайной короткой ссылки."""
        while True:
            short = ''.join(
                sample(ACCEPTABLE_SYMBOLS, LINK_LENGTH),
            )
            if not URLMap.check_uniqueness_short(short):
                return short

    @staticmethod
    def create_url_map(original, short):
        """Метод создания новой записи в базе данных."""
        if not short:
            short = URLMap.get_unique_short()
        if URLMap.check_uniqueness_short(short):
            raise ObjectCreationException(UNIQUE_ERROR_MESSAGE)
        if len(short) > MAX_LENGTH_SHORT_URL:
            raise ObjectCreationException(MAX_LENGTH_ERROR_MESSAGE)
        if not re.compile(R_STRING).search(short):
            raise ObjectCreationException(WRONG_NAME_ERROR_MESSAGE)
        url_map = URLMap(
            original=original,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
