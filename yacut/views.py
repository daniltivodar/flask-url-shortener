from http import HTTPStatus

from flask import abort, flash, redirect, render_template
from yacut import app
from yacut.error_handlers import ObjectCreationException
from yacut.forms import UrlForm
from yacut.models import URLMap

UNIQUE_ERROR_MESSAGE = 'Предложенный вариант короткой ссылки уже существует.'


@app.route('/<string:short>', methods=('GET',))
def short_redirect_view(short):
    """Редиректит на оригинальную страницу по короткой ссылке."""
    url_map = URLMap.check_uniqueness_short(short)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)


@app.route('/', methods=('GET', 'POST'))
def index_view():
    """Метод главной страницы с формой создания короткой ссылки."""
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create_url_map(
            form.original_link.data,
            form.custom_id.data,
        )
    except ObjectCreationException as error:
        flash(error)
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        short=url_map.get_short_redirect_url(),
    )
