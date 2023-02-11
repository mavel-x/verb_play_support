# VerbPlay Support Bot

Powered by Google Dialogflow

## Установка и настройка

### Проект Google Cloud
1. Создать Service Account для проекта
2. Создать API ключ к нему и добавить путь к JSON-файлу с данными авторизации
в переменную GOOGLE_APPLICATION_CREDENTIALS в файле `.env`
3. Добавить в разделе IAM в консоли Google Cloud необходимые разрешения для этого сервисного аккаунта: 
Dialogflow API Client, Dialogflow Intent Admin