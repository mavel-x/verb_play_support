import json

import vk_api
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from dialog_handler import detect_intent_for_text


def main():
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
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            detection_result = detect_intent_for_text(gc_project_id, event.user_id, event.text)
            if detection_result.intent.is_fallback:
                continue
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message=detection_result.fulfillment_text,
            )


if __name__ == '__main__':
    main()
