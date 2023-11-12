from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Regexp

from .constants import MATCH_SHORT_LINK


class YacutForm(FlaskForm):
    original_link = URLField(
        "Ваша длинная ссылка",
        validators=[
            DataRequired(message="Это обязательное поле!"),
            URL(message="Некорректный URL!"),
            Length(1, 256),
        ],
    )

    custom_id = StringField(
        "Ваш вариант короткой ссылки (не более 16 символов)",
        validators=[
            Length(0, 16),
            Regexp(
                MATCH_SHORT_LINK, message="Ссылка должна содержать допустимые символы!"
            ),
        ],
    )

    submit = SubmitField("Создать")
