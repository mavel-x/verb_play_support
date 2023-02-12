import logging

import telegram


class TGLogHandler(logging.Handler):

    def __init__(self, tg_bot: telegram.Bot, tg_user: int):
        self.tg_bot = tg_bot
        self.tg_user = tg_user
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.tg_user, text=log_entry)


def configure_tg_alerts(target_logger: logging.Logger, bot_token: str, recipient_user_id: int | str):
    bot = telegram.Bot(bot_token)
    tg_handler = TGLogHandler(bot, recipient_user_id)
    tg_handler.setLevel(logging.WARNING)
    target_logger.addHandler(tg_handler)

