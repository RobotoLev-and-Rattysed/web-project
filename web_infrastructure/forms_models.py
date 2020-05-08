from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, IntegerField, FileField, SubmitField
from wtforms import BooleanField, SelectField
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


class BookForm(FlaskForm):
    name = StringField('Название книги', validators=[DataRequired()])
    author = SelectField('Автор', coerce=int, validate_choice=False)
    genre = SelectField('Жанр', coerce=int, validate_choice=False)
    description = TextAreaField('Описание книги (если оставить пустым, '
                                'автоматически сформируется с использованием Википедии)')

    edit_image = BooleanField('Отметьте, если хотите изменить картинку книги')
    image = FileField('Изображение книги')
    edit_text = BooleanField('Отметьте, если хотите изменить прикрепленный текст')
    text = FileField('Текст книги')

    submit = SubmitField('Сохранить')


class DeleteForm(FlaskForm):
    submit = SubmitField('Удалить объект')


class AuthorForm(FlaskForm):
    name = StringField('ФИО автора', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class GenreForm(FlaskForm):
    name = StringField('Название жанра', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
