import html
import json
import logging

import telegram.ext
from environs import Env
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialog_handler import detect_intent_for_text


logger = logging.getLogger('tg_bot')


def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the admin."""
    logger.error(msg='Exception while handling an update:', exc_info=context.error)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update:\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n'
        f'<pre>{html.escape(str(context.error))}</pre>'
    )
    context.bot.send_message(
        chat_id=context.bot_data['admin_chat_id'], text=message, parse_mode=ParseMode.HTML
    )


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте.')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def detect_message_intent(update: Update, context: CallbackContext) -> None:
    detection_result = detect_intent_for_text(
        project_id=context.bot_data['gc_project_id'],
        session_id=update.effective_user.id,
        text=update.message.text,
    )
    update.message.reply_text(detection_result.fulfillment_text)


def run_tg_bot(tg_token, gc_project_id, admin_chat_id):
    updater = Updater(tg_token)
    dispatcher: telegram.ext.Dispatcher = updater.dispatcher
    dispatcher.bot_data.update({
        'gc_project_id': gc_project_id,
        'admin_chat_id': admin_chat_id,
    })
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_message_intent))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


def main() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    env = Env()
    env.read_env()

    tg_token = env.str('TG_TOKEN')
    admin_chat_id = env.int('ADMIN_TG_CHAT')

    with open(env.path('GOOGLE_APPLICATION_CREDENTIALS'), 'r') as file:
        gc_credentials = json.load(file)
        gc_project_id = gc_credentials['project_id']

    run_tg_bot(tg_token, gc_project_id, admin_chat_id)


if __name__ == '__main__':
    main()
