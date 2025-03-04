from random import choice
from string import ascii_lowercase, ascii_uppercase, digits

from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.constants import (
    FLASH_CATEGORY,
    FLASH_CATEGORY_ERROR,
    GET_URL_ERROR_MESSAGE,
    LINK_LENGTH,
    UNIQUE_ERROR_MESSAGE,
)
from yacut.error_handlers import InvalidAPIUsage
from yacut.forms import UrlForm
from yacut.models import URLMap


def get_unique_short_id():
    """Метод создания случайной короткой ссылки."""
    return ''.join(
        choice(ascii_lowercase + ascii_uppercase + digits)
        for char in range(LINK_LENGTH)
    )


@app.route('/<string:short_link>', methods=('GET',))
def short_redirect_view(short_link):
    """Редиректит на оригинальную страницу по короткой ссылке."""
    url_lists = URLMap.query.filter_by(short=short_link).first()
    if not url_lists:
        raise InvalidAPIUsage(GET_URL_ERROR_MESSAGE, 404)
    return redirect(url_lists.original)


@app.route('/', methods=('GET', 'POST'))
def index_view():
    """Метод главной страницы с формой создания короткой ссылки."""
    form = UrlForm()
    if form.validate_on_submit():
        if not form.custom_id.data:
            form.custom_id.data = get_unique_short_id()
        if URLMap.query.filter_by(short=form.custom_id.data).first():
            flash(UNIQUE_ERROR_MESSAGE, FLASH_CATEGORY_ERROR)
            return render_template('index.html', form=form)
        url_links = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
        db.session.add(url_links)
        db.session.commit()
        flash(
            url_for(
                'short_redirect_view',
                short_link=form.custom_id.data,
                _external=True,
            ),
            FLASH_CATEGORY,
        )
    return render_template('index.html', form=form)
