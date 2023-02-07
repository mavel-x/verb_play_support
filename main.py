import json
import logging

import telegram.ext
from google.cloud import dialogflow
from environs import Env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте.')


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help text')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def detect_intent_for_text(project_id, session_id, text, language_code='ru'):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print(f'Session path: {session}\n')

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print('=' * 20)
    print(f'Query text: {response.query_result.query_text}')
    print(
        'Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print(f'Fulfillment text: {response.query_result.fulfillment_text}\n')


def detect_message_intent(update: Update, context: CallbackContext) -> None:
    return detect_intent_for_text(
        project_id=context.bot_data['gc_project_id'],
        session_id=update.effective_user.id,
        text=update.message.text,
    )


def main() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    env = Env()
    env.read_env()

    with open(env.path('GOOGLE_APPLICATION_CREDENTIALS'), 'r') as file:
        gc_credentials = json.load(file)
        gc_project_id = gc_credentials['project_id']


    updater = Updater(env.str('TG_TOKEN'))
    dispatcher: telegram.ext.Dispatcher = updater.dispatcher
    dispatcher.bot_data['gc_project_id'] = gc_project_id

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_message_intent))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
