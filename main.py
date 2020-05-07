from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
# from flask_ngrok import run_with_ngrok

from bots_handlers import vk_handler
from web_infrastructure import web_main, users_blueprint, books_blueprint, book_data_blueprint, \
    requests_blueprint
from web_infrastructure.API import book_resource

from data import db_session
from data.db_session import User
from settings import csrf_key

import os


db_session.global_init()


app = Flask(__name__)
app.config['SECRET_KEY'] = csrf_key


api = Api(app)
api.add_resource(book_resource.BookResource, '/api/v1/book/<int:book_id>')
api.add_resource(book_resource.BookListResource, '/api/v1/books')


login_manager = LoginManager()
login_manager.init_app(app)


app.register_blueprint(vk_handler.blueprint)

app.register_blueprint(web_main.blueprint)
app.register_blueprint(users_blueprint.blueprint)
app.register_blueprint(books_blueprint.blueprint)
app.register_blueprint(book_data_blueprint.blueprint)
app.register_blueprint(requests_blueprint.blueprint)


# run_with_ngrok(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port=port)
    # app.run()
