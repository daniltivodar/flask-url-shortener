import re

from flask import jsonify, request

from yacut import app, db
from yacut.constants import (
    EMPTY_BODY_ERROR_MESSAGE,
    EMPTY_URL_ERROR_MESSAGE,
    GET_URL_ERROR_MESSAGE,
    MAX_LENGTH_ERROR_MESSAGE,
    R_STRING,
    WRONG_NAME_ERROR_MESSAGE,
)
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import UNIQUE_ERROR_MESSAGE, get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_url(short_id):
    url_lists = URLMap.query.filter_by(short=short_id).first()
    if not url_lists:
        raise InvalidAPIUsage(GET_URL_ERROR_MESSAGE, 404)
    return jsonify({'url': url_lists.original}), 200


@app.route('/api/id/', methods=('POST',))
def create_url():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(EMPTY_BODY_ERROR_MESSAGE)
    if 'url' not in data:
        raise InvalidAPIUsage(EMPTY_URL_ERROR_MESSAGE)
    if 'custom_id' not in data or data['custom_id'] == '':
        data['custom_id'] = get_unique_short_id()
    if len(data['custom_id']) > 16:
        raise InvalidAPIUsage(MAX_LENGTH_ERROR_MESSAGE)
    if not re.compile(R_STRING).search(data['custom_id']):
        raise InvalidAPIUsage(WRONG_NAME_ERROR_MESSAGE)
    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage(UNIQUE_ERROR_MESSAGE)
    urls_list = URLMap()
    urls_list.from_dict(data)
    db.session.add(urls_list)
    db.session.commit()
    return jsonify(urls_list.to_dict()), 201
