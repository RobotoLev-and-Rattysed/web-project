from flask import Blueprint, request
from flask_login import login_user, logout_user, current_user, login_required


blueprint = Blueprint(__name__, 'web')


@blueprint.route('/')
def main():
    return "Hello World!"
