from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import MAX_LENGTH_ORIGINAL_URL, MAX_LENGTH_SHORT_URL, R_STRING

REQUIRED_FIELD = 'Обязательное поле'
ORIGINAL_LINK_LABEL = 'Длинная ссылка'
SHORT_LINK_LABEL = 'Ваш вариант короткой ссылки'
SUBMIT_LINK_LABEL = 'Создать'


class UrlForm(FlaskForm):
    """Форма создания короткой ссылки."""

    original_link = URLField(
        ORIGINAL_LINK_LABEL,
        validators=(
            DataRequired(message=REQUIRED_FIELD),
            Length(max=MAX_LENGTH_ORIGINAL_URL),
        ),
    )
    custom_id = StringField(
        SHORT_LINK_LABEL,
        validators=(
            Length(max=MAX_LENGTH_SHORT_URL),
            Optional(),
            Regexp(regex=R_STRING),
        ),
    )
    submit = SubmitField(SUBMIT_LINK_LABEL)
