from datetime import datetime as dt
from random import sample
import re

from flask import url_for

from settings import (
    ACCEPTABLE_SYMBOLS,
    ATTEMPS_COUNT,
    SHORT_LENGTH,
    MAX_LENGTH_ORIGINAL_URL,
    MAX_LENGTH_SHORT,
    PATTERN,
    SHORT_REDIRECT_VIEW,
)
from yacut import db

GET_UNIQUE_SHORT_ERROR = 'Не удалось создать уникальную короткую ссылку.'
UNIQUE_ERROR_MESSAGE = 'Предложенный вариант короткой ссылки уже существует.'
WRONG_ORIGINAL_NAME_ERROR_MESSAGE = (
    'Указано недопустимое имя для оригинальной ссылки'
)
WRONG_SHORT_NAME_ERROR_MESSAGE = 'Указано недопустимое имя для короткой ссылки'


class URLMap(db.Model):
    """Модель сохранения ссылок и их коротких версий."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL_URL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT))
    timestamp = db.Column(db.DateTime, index=True, default=dt.now)

    class ObjectCreationException(Exception):
        """Класс для обработки исключений при создании объекта модели."""

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_short_redirect_url(),
        )

    def get_short_redirect_url(self):
        return url_for(
            SHORT_REDIRECT_VIEW,
            short=self.short,
            _external=True,
        )

    @staticmethod
    def get_uniqueness_short(short):
        """Проверяет уникальность короткой ссылки."""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short():
        """Метод создания случайной короткой ссылки."""
        for attempt in range(ATTEMPS_COUNT):
            short = ''.join(
                sample(ACCEPTABLE_SYMBOLS, SHORT_LENGTH),
            )
            if not URLMap.get_uniqueness_short(short):
                return short
        raise URLMap.ObjectCreationException(GET_UNIQUE_SHORT_ERROR)

    @staticmethod
    def create(original, short, validation=False):
        """Метод создания новой записи в базе данных."""
        if validation:
            if len(original) > MAX_LENGTH_ORIGINAL_URL:
                raise URLMap.ObjectCreationException(
                    WRONG_ORIGINAL_NAME_ERROR_MESSAGE,
                )
        if short:
            if URLMap.get_uniqueness_short(short):
                raise URLMap.ObjectCreationException(UNIQUE_ERROR_MESSAGE)
        else:
            short = URLMap.get_unique_short()
        if validation:
            if len(short) > MAX_LENGTH_SHORT:
                raise URLMap.ObjectCreationException(
                    WRONG_SHORT_NAME_ERROR_MESSAGE,
                )
            if not re.compile(PATTERN).search(short):
                raise URLMap.ObjectCreationException(
                    WRONG_SHORT_NAME_ERROR_MESSAGE,
                )
        url_map = URLMap(
            original=original,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
