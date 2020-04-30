import os.path as path
import random


chars = [chr(i) for i in range(48, 58)] + [chr(i) for i in range(97, 123)]


def get_photo_by_book(book):
    image_url = '/static/img/books/no_image.jpg'
    if book and book.image:
        image_name = ''.join(random.choice(chars) for _ in range(32))
        image_url = f'/static/img/books/{image_name}.jpg'
        with open(path.abspath(path.join(__file__, '../..' + image_url)), 'wb') as f:
            f.write(book.image)

    return image_url
