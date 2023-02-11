import json
import logging

import vk_api
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from dialog_handler import get_reply_to_text

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    env = Env()
    env.read_env()

    with open(env.path('GOOGLE_APPLICATION_CREDENTIALS'), 'r') as file:
        gc_credentials = json.load(file)
        gc_project_id = gc_credentials['project_id']

    vk_token = env.str('VK_API_KEY')
    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)

            reply = get_reply_to_text(gc_project_id, event.user_id, event.text)

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message=reply,
            )


if __name__ == '__main__':
    main()
