import os

os.system('heroku pg:credentials:rotate DATABASE -a=yandexlyceum-web-project '
          '--confirm yandexlyceum-web-project')
os.system('heroku pg:credentials:url -a=yandexlyceum-web-project')


print('=======')
print('Доступы успешно сброшены')
print('Замените database_url в settings.py на выведенный выше Connection URL')
