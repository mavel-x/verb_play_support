import json
import logging

import google
from environs import Env
from google.cloud import dialogflow

logger = logging.getLogger(__name__)


def create_intent(project_id, display_name, training_phrases_parts, answer_text):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=[answer_text])
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    response = intents_client.create_intent(
        request={'parent': parent, 'intent': intent}
    )
    logger.info(f'Intent created: {response}')


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    env = Env()
    env.read_env()

    with open(env.path('GOOGLE_APPLICATION_CREDENTIALS'), 'r') as file:
        gc_credentials = json.load(file)
        gc_project_id = gc_credentials['project_id']

    with open(env.path('INTENTS_PATH'), 'r') as file:
        intents = json.load(file)

    for intent_name, intent_settings in intents.items():
        try:
            create_intent(gc_project_id, intent_name, intent_settings['questions'], intent_settings['answer'])
        except google.api_core.exceptions.InvalidArgument:
            continue


if __name__ == '__main__':
    main()
