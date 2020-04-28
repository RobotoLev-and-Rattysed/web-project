import os
from data import db_session
from data.db_session import User, Book, Genre, Author


os.system('heroku pg:reset DATABASE -a yandexlyceum-web-project --confirm yandexlyceum-web-project')

db_session.global_init()
session = db_session.create_session()

user = User(email='user@test.ru')
user.set_password('user')
moderator = User(email='moderator@test.ru', is_moderator=True)
moderator.set_password('moderator')

session.add(user)
session.add(moderator)
session.add(Author(name='Тестовый автор'))
session.add(Genre(name='Тестовый жанр'))
session.add(Book(user_id=1,
                 name='Тестовая книга',
                 author_id=1,
                 genre_id=1))

session.commit()
