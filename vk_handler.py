from flask import Blueprint, request
import vk

import json
import random

from settings import group_key, confirmation_key, secret_key


blueprint = Blueprint(__name__, 'vk_handler')

session = vk.Session()
api = vk.API(session, v='5.103')


@blueprint.route('/vk_callback', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'secret' not in data or data['secret'] != secret_key:
        return 'access denied'
    if 'type' not in data:
        return 'error'
    elif data['type'] == 'confirmation':
        return confirmation_key
    elif data['type'] == 'message_new':
        message = data['object']['message']
        api.messages.send(access_token=group_key, user_id=message['from_id'],
                          message=f'Я получил сообщение \"{message["text"]}\"',
                          random_id=random.randint(0, 2 ** 64))
        return 'ok'
