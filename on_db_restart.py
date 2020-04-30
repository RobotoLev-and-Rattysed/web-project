import os
from data import db_session
from data.db_session import User, Book, Genre, Author


os.system('heroku pg:reset DATABASE -a yandexlyceum-web-project --confirm yandexlyceum-web-project')


db_session.global_init()
session = db_session.create_session()


user = User(email='user@test.ru', nickname='User')
user.set_password('user')
session.add(user)
moderator = User(email='moderator@test.ru', nickname='Moderator', is_moderator=True)
moderator.set_password('moderator')
session.add(moderator)
test = User(email='test@test.ru', nickname='Test')
test.set_password('test')
session.add(test)

session.add(Author(name='Тестовый автор'))
session.add(Genre(name='Тестовый жанр'))

for i in range(1, 7):
    book = Book(user_id=1,
                name=f'Тестовая книга {i}',
                author_id=1,
                genre_id=1)

    if i % 2 == 0:
        book.user_id = 2

    if i % 3 == 1:
        book.status = -1
    elif i % 3 == 0:
        book.status = 1

    if i == 1:
        book.image = 'static/img/books/test.jpg'

    session.add(book)


session.commit()
print('База успешно обновлена')
