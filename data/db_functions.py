import os.path as path
import random


chars = [chr(i) for i in range(48, 58)] + [chr(i) for i in range(97, 123)]


def generate_random_filename(length=64, extension=''):
    return ''.join(random.choice(chars) for _ in range(length)) + extension


def get_text_by_book(book):
    if not book:
        return

    text_name = book.text_name
    text_url = f'/static/txt/books/{text_name}'

    absolute_text_path = path.abspath(path.join(__file__, '../..' + text_url))
    if not path.isfile(absolute_text_path):
        with open(absolute_text_path, 'wb') as f:
            f.write(book.text)

    return text_url


def set_text_by_book(book, text_name):
    if not book or not text_name:
        return

    book.text_name = text_name
    text_url = f'/static/txt/books/{text_name}'
    with open(path.abspath(path.join(__file__, '../..' + text_url)), 'rb') as f:
        book.text = f.read()


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
    if image_name == 'no_image.jpg':
        book.image = None
    else:
        image_url = f'/static/img/books/{image_name}'
        with open(path.abspath(path.join(__file__, '../..' + image_url)), 'rb') as f:
            book.image = f.read()
