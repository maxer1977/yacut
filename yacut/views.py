from flask import flash, redirect, render_template

from . import app, db
from .forms import YacutForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if form.validate_on_submit():
        link = URLMap()

        original = form.original_link.data

        short = form.custom_id.data
        # если имя для короткой ссылки не задано
        if not short:
            # используем функцию автоформирования имени
            short = link.get_unique_short_id()
            # в случае совпадения этого имени с существующим
            # перезапускается автоформирование
            while URLMap.query.filter_by(short=short).first():
                short = link.get_unique_short_id()

        if URLMap.query.filter_by(short=short).first():
            # проверка, что предоставленное короткое имя уникально
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)

        # запись и сохранение данных в БД
        link.original = original
        link.short = short
        db.session.add(link)
        db.session.commit()

        # Отрисовка заполненной формы с формированной короткой ссылкой
        return render_template('index.html', form=form, short=short)
    # Отрисовка пустой формы
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET', ])
def link_view(short):
    # получение имени короткой ссылки или 404
    link_entry = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(link_entry.original, code=302)
