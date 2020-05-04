import os.path as path
import random


chars = [chr(i) for i in range(48, 58)] + [chr(i) for i in range(97, 123)]


def generate_random_filename(length=32, extension=''):
    return ''.join(random.choice(chars) for _ in range(length)) + extension


def get_image_by_book(book):
    image_name = book.image_name
    image_url = f'/static/img/books/{image_name}'

    absolute_image_path = path.abspath(path.join(__file__, '../..' + image_url))
    if not path.isfile(absolute_image_path):
        with open(absolute_image_path, 'wb') as f:
            f.write(book.image)

    return image_url


def set_image_by_book(book, image_name):
    if not book or not image_name:
        return

    book.image_name = image_name
    image_url = f'/static/img/books/{image_name}'
    with open(path.abspath(path.join(__file__, '../..' + image_url)), 'rb') as f:
        book.image = f.read()
