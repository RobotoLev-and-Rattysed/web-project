from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, IntegerField, FileField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    nickname = StringField('Желаемый никнейм', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class NewBookForm(FlaskForm):
    name = StringField('Название книги', validators=[DataRequired()])
    author = IntegerField('ID автора', validators=[DataRequired()])
    genre = IntegerField('ID жанра', validators=[DataRequired()])
    description = TextAreaField('Описание книги', validators=[DataRequired()])
    image = FileField('Изображение книги')
    submit = SubmitField('Добавить книгу')
