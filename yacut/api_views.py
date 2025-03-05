from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap

EMPTY_BODY_ERROR_MESSAGE = 'Отсутствует тело запроса'
EMPTY_URL_ERROR_MESSAGE = '"url" является обязательным полем!'
GET_URL_ERROR_MESSAGE = 'Указанный id не найден'


@app.route('/api/id/<string:short>/', methods=('GET',))
def get_url(short):
    url_map = URLMap.get_uniqueness_short(short)
    if not url_map:
        raise InvalidAPIUsage(GET_URL_ERROR_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=('POST',))
def create_url():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(EMPTY_BODY_ERROR_MESSAGE)
    if 'url' not in data:
        raise InvalidAPIUsage(EMPTY_URL_ERROR_MESSAGE)
    try:
        url_map = URLMap.create(data['url'], data.get('custom_id'), True)
    except URLMap.ObjectCreationException as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
