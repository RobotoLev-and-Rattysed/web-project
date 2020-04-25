from flask import Flask, request, redirect
from flask_login import LoginManager
# from flask_ngrok import run_with_ngrok

import vk_handler
import web

from data import db_session
from data.db_session import User
from settings import csrf_key

import os


db_session.global_init()

app = Flask(__name__)
app.config['SECRET_KEY'] = csrf_key
app.register_blueprint(vk_handler.blueprint)
app.register_blueprint(web.blueprint)

# run_with_ngrok(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


# Автоматический редирект с http:// на https://, если запрашиваемый адрес существует
# При локальном тестировании надо закомментировать всю функцию
@app.before_request
def force_https():
    if not request.is_secure:
        return redirect(request.url.replace('http://', 'https://'), 301)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port=port)
    # app.run()
