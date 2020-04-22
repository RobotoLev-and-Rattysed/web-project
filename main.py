from flask import Flask
# from flask_ngrok import run_with_ngrok

import vk_handler
from data import db_session

import os


db_session.global_init()

app = Flask(__name__)
app.register_blueprint(vk_handler.blueprint)
# run_with_ngrok(app)


@app.route('/')
def main():
    return "Hello World!"


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port=port)
    # app.run()
