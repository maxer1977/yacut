from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def make_short_link():
    # создаем пустой экземпляра модели
    link = URLMap()

    data = request.get_json()

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    # добавляем значение исходной ссылки
    link.original = data['url']

    # автоформирование короткого имени для отсутствующего
    # или пустого короткого имени
    if 'custom_id' not in data or not data['custom_id']:
        link.short = link.get_unique_short_id()

    else:
        if len(data['custom_id']) > 16 or not link.check_link(data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

        if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')

        # использование предоставленного короткого имени
        link.short = data['custom_id']

    # добавление и сохранение новой записи в БД
    db.session.add(link)
    db.session.commit()

    return jsonify(link.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):

    link = URLMap.query.filter_by(short=short).first()

    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify({'url': link.original}), 200
