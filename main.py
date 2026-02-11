import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

# === НАСТРОЙКИ ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Хранилище контекста диалогов
# chat_id -> list[dict]
dialog_history = {}

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("Новый запрос")]],
    resize_keyboard=True,
)

# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
def reset_context(chat_id: int):
    dialog_history[chat_id] = [
        {"role": "system", "content": "Ты полезный и точный ассистент."}
    ]


# === ОБРАБОТЧИКИ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    reset_context(chat_id)

    await update.message.reply_text(
        "Контекст диалога сброшен.\nОтправьте сообщение для нового запроса.",
        reply_markup=keyboard,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — сбросить контекст\n"
        "Любое сообщение — запрос к ChatGPT\n"
        "Кнопка «Новый запрос» — начать заново",
        reply_markup=keyboard,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text

    # Обработка кнопки
    if user_text == "Новый запрос":
        reset_context(chat_id)
        await update.message.reply_text(
            "Контекст очищен. Введите новый запрос.",
            reply_markup=keyboard,
        )
        return

    # Инициализация контекста при первом сообщении
    if chat_id not in dialog_history:
        reset_context(chat_id)

    # Добавляем сообщение пользователя в историю
    dialog_history[chat_id].append(
        {"role": "user", "content": user_text}
    )

    # Запрос к ChatGPT
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=dialog_history[chat_id],
        temperature=0.7,
    )

    assistant_text = response.choices[0].message.content

    # Добавляем ответ ассистента в контекст
    dialog_history[chat_id].append(
        {"role": "assistant", "content": assistant_text}
    )

    await update.message.reply_text(
        assistant_text,
        reply_markup=keyboard,
    )


# === ЗАПУСК ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()



