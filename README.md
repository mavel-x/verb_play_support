# VerbPlay Support Bot

Бот для ответов на часто задаваемые вопросы к техподдержке издательства "Игра глаголов".

## Установка и настройка

### Установка зависимостей
1. Создать виртуальное окружение и установить в него необходимые библиотеки:
   ```commandline
   python3 -m venv venv
   venv/bin/pip install -U -r requirements.txt 
   ```
1. Создать файл `.env` в корневой директории проекта и добавьте в него переменную со своим user id в телеграме (для получения сообщений об ошибках):
   ```commandline
   ADMIN_TG_CHAT=1234567
   ```
   Также туда нужно будет добавить переменные из следующих разделов.

### Проект Google Cloud
1. Создать проект на Google Cloud
1. Создать агента Dialogflow в этом проекте 
1. Создать Service Account для проекта
1. Создать API ключ к нему и добавить путь к JSON-файлу с данными авторизации
в переменную GOOGLE_APPLICATION_CREDENTIALS в файле `.env`
1. Добавить в разделе IAM в консоли Google Cloud необходимые разрешения для этого сервисного аккаунта: 
Dialogflow API Client, Dialogflow Intent Admin

### Бот для Телеграма
1. Создать бота через BotFather
2. Добавить его токен в переменную TG_TOKEN в файле `.env`

### Бот для ВК
1. Создать сообщество
2. В настройках сообщества разрешить боту отправку сообщений
3. Добавить токен бота в переменную VK_API_KEY в файле `.env`

### Обучение диалоговой нейросети
1. Получить JSON-файл с частыми вопросами и ответами
2. Добавить путь к нему в переменную INTENTS_PATH в файле `.env`
3. Запустить скрипт `train_agent.py`

## Использование
ВК-бот и телеграм-бот работают из файлов `vk_bot.py` и `tg_bot.py`.
Для параллельного запуска на сервере вам поможет, например, утилита 
[screens](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Hosting-your-bot#start-your-bot).

## О проекте
Это учебный проект для школы Python-разработчиков [dvmn.org](https://dvmn.org).
