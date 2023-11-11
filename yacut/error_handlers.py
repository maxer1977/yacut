from http import HTTPStatus

from flask import jsonify, render_template, request

from . import app


class InvalidAPIUsage(Exception):
    # статус-код по умолчанию
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        # если статус-код передан в конструктор —
        # этот код вернётся в ответе
        if status_code is not None:
            self.status_code = status_code

    # Метод для сериализации переданного сообщения об ошибке
    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(404)
def page_not_found(error):
    url = request.url
    return render_template('404.html', url=url), HTTPStatus.NOT_FOUND


@app.errorhandler(500)
def internal_error(error):
    url = request.url
    return render_template('500.html', url=url), HTTPStatus.INTERNAL_SERVER_ERROR


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code
