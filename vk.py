import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import random


api_token = '7826c95a31893273c01d1f66427239c828fd6099c5717149a38e063127e55f4d6205db40fd048b63ef42d'


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
