from flask import Blueprint, request
import vk

import os.path as path
import requests
import json
import random

from settings import vk_group_key, vk_confirmation_key, vk_secret_key
from bots_infrastructure.bot_engine import get_answer

blueprint = Blueprint(__name__, 'vk_handler')

session = vk.Session()
api = vk.API(session, v='5.103')


@blueprint.route('/vk_callback', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'secret' not in data or data['secret'] != vk_secret_key:
        return 'access denied'
    if 'type' not in data:
        return 'error'
    elif data['type'] == 'confirmation':
        return vk_confirmation_key
    elif data['type'] == 'message_new':
        message = data['object']['message']
        peer_id = data['object']['message']['peer_id']

        answer = get_answer(message['text'], platform='vk')

        if answer.text or answer.attachments:
            # print(answer.attachments.values())
            # print([save_attachments(peer_id, file_type, file_paths)
            #        for file_type, file_paths in answer.attachments.values()])
            # return 'ok'
            attachment = None
            if answer.attachments:
                attachment = ','.join([save_attachments(peer_id, file_type, file_paths)
                                       for file_type, file_paths in answer.attachments.items()])
            api.messages.send(access_token=vk_group_key, peer_id=message['peer_id'],
                              message=answer.text, attachment=attachment,
                              random_id=random.randint(0, 2 ** 64))
        return 'ok'


def save_attachments(peer_id, file_type, file_paths) -> str:
    if file_type == 'photo':
        return ','.join([save_photo(peer_id, path.abspath(path.join(__file__, '../..' + file_path))
                                    ) for file_path in file_paths])
    elif file_type == 'text':
        return ','.join(
            [save_document(peer_id, path.abspath(path.join(__file__, '../..' + file_path)))
             for file_path in file_paths])
    else:
        return ''


def save_photo(peer_id, file_path) -> str:
    upload_url = api.photos.getMessagesUploadServer(access_token=vk_group_key,
                                                    peer_id=peer_id)['upload_url']
    vk_loader_response = requests.post(
        upload_url,
        files={'photo': open(file_path, 'rb')}
    ).json()
    vk_saver_response = api.photos.saveMessagesPhoto(
        access_token=vk_group_key,
        server=vk_loader_response['server'],
        photo=vk_loader_response['photo'],
        hash=vk_loader_response['hash']
    )

    attachment = f"photo{vk_saver_response[0]['owner_id']}_" \
                 f"{vk_saver_response[0]['id']}_" \
                 f"{vk_saver_response[0]['access_key']}"
    return attachment


def save_document(peer_id, file_path) -> str:
    upload_url = api.docs.getMessagesUploadServer(type='doc',
                                                  access_token=vk_group_key,
                                                  peer_id=peer_id)['upload_url']
    vk_loader_response = requests.post(
        upload_url,
        files={'file': open(file_path, 'rb')}
    ).json()
    vk_saver_response = api.docs.save(
        access_token=vk_group_key,
        file=vk_loader_response['file']
    )

    attachment = f"doc{vk_saver_response['doc']['owner_id']}_" \
                 f"{vk_saver_response['doc']['id']}"
    return attachment
