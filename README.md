
---

# Telegram GPT Bot

Телеграм-бот с использованием OpenAI API.
Бот поддерживает контекст диалога и позволяет сбрасывать его через команду `/start` или кнопку «Новый запрос».

---

## Требования

* Python 3.11+
* Telegram Bot Token
* OpenAI API Key

---

## Установка

1. Клонировать проект:

```
git clone <repo_url>
cd project
```

2. Создать виртуальное окружение:

```
py -3.11 -m venv venv
venv\Scripts\activate
```

3. Установить зависимости:

```
pip install -r requirements.txt
```

---

## Настройка переменных окружения

В целях безопасности API-ключи не хранятся в коде (OpenAI ключ не выкладываю на Github в тех же целях).

Установите их вручную через терминал (PowerShell):

```
setx TELEGRAM_BOT_TOKEN "8290296948:AAFO8ambDw0m7Siamqdxh5exXp43m6FbR3Y"
setx OPENAI_API_KEY "your_openai_key_here"
```

После выполнения команд перезапустите терминал.

---

## Запуск

```
python main.py
```
