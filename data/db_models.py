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
    is_moderator = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    books = orm.relation("Book", back_populates='user_object')

    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    # jobs = orm.relation("Jobs", back_populates='team_leader_object')
    # departments = orm.relation("Department", back_populates='chief_object')

    def __repr__(self):
        return f'<User> {self.id} {self.login}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('authors.id'))
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('genres.id'))

    user_object = orm.relation('User')
    author_object = orm.relation('Author')
    genre_object = orm.relation('Genre')

    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)


class Author(SqlAlchemyBase):
    __tablename__ = 'authors'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)

    books = orm.relation('Book', back_populates='author_object')

    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)


class Genre(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Integer, unique=True)

    books = orm.relation('Book', back_populates='genre_object')

    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
