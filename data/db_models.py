import datetime
import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, unique=True)
    is_moderator = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    books = orm.relationship("Book", back_populates='user')

    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    # jobs = orm.relation("Jobs", back_populates='team_leader_object')
    # departments = orm.relation("Department", back_populates='chief_object')

    def __repr__(self):
        return f'<User> {self.id} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))

    name = sqlalchemy.Column(sqlalchemy.String)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('authors.id'))
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('genres.id'))
    user = orm.relationship('User', back_populates='books')
    author = orm.relationship('Author', back_populates='books')
    genre = orm.relationship('Genre', back_populates='books')

    description = sqlalchemy.Column(sqlalchemy.String, default='Нет описания :(')
    image = sqlalchemy.Column(sqlalchemy.String, default='static/img/books/no_image.jpg')
    status = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)


class Author(SqlAlchemyBase):
    __tablename__ = 'authors'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)

    books = orm.relation('Book', back_populates='author')

    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)


class Genre(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)

    books = orm.relation('Book', back_populates='genre')

    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
