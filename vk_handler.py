from flask import Blueprint, request
import vk

import json
import random

from settings import group_key, confirmation_key, secret_key
from bot_engine import get_answer


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

        answer_text, answer_attachment = get_answer(message['text'], platform='vk')

        if answer_text or answer_attachment:
            api.messages.send(access_token=group_key, peer_id=message['peer_id'],
                              message=answer_text, attachment=answer_attachment,
                              random_id=random.randint(0, 2 ** 64))
        return 'ok'
