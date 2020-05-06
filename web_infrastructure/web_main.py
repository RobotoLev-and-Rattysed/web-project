from flask import Blueprint, render_template


blueprint = Blueprint(__name__, 'web_main', template_folder='templates')


@blueprint.route('/')
def main():
    return render_template('greeting.html', title='Электронная библиотека')
