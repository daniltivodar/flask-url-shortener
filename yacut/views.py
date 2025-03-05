from http import HTTPStatus

from flask import abort, flash, redirect, render_template
from yacut import app
from yacut.forms import UrlForm
from yacut.models import URLMap


@app.route('/<string:short>', methods=('GET',))
def short_redirect_view(short):
    """Редиректит на оригинальную страницу по короткой ссылке."""
    url_map = URLMap.get_uniqueness_short(short)
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
        url_map = URLMap.create(
            form.original_link.data,
            form.custom_id.data,
        )
    except URLMap.ObjectCreationException as error:
        flash(error)
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        link=url_map.get_short_redirect_url(),
    )


@app.route('/redoc')
def get_api_documentation():
    return render_template('redoc.html')
