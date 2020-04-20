import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import random


api_token = 'bc1e91d1bdb31d5347620628e04b7cfecf4107c57b1ffd1e2133d8e8a44872db16cbfa953ba2d63ef89e8'


vk_session = vk_api.VkApi(token=api_token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 194404073)


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.obj.message
        from_id = message['from_id']
        text = message['text']

        vk.messages.send(user_id=from_id, message='Сообщение принято и обработано',
                         random_id=random.randint(0, 2 ** 64))
