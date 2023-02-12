import json
import logging

import vk_api
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from dialog_handler import detect_intent_for_text
from log_handlers import configure_tg_alerts

logger = logging.getLogger('vk_bot')


def run_vk_bot(vk_token, gc_project_id):
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


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    env = Env()
    env.read_env()

    tg_token = env.str('TG_TOKEN')
    admin_tg_chat = env.int('ADMIN_TG_CHAT')
    configure_tg_alerts(logger, tg_token, admin_tg_chat)

    vk_token = env.str('VK_API_KEY')
    with open(env.path('GOOGLE_APPLICATION_CREDENTIALS'), 'r') as file:
        gc_credentials = json.load(file)
        gc_project_id = gc_credentials['project_id']

    try:
        run_vk_bot(vk_token, gc_project_id)
    except Exception as e:
        logger.error(f'VK-бот упал с ошибкой:\n{e}')
        raise


if __name__ == '__main__':
    main()
