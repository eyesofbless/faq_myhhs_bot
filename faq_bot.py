import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# ============================
# НАСТРОЙКИ
# ============================


# ============================
# FAQ - ВОПРОСЫ И ОТВЕТЫ
# Редактируй под своего клиента!
# ============================
FAQ = {
    "💰 Цены и оплата": "Оплата производится на карту или через PayPal. Цены обсуждаются индивидуально. Напишите нам для расчёта стоимости.",
    "⏰ Сроки работы": "Работаем с 9:00 до 21:00 по московскому времени. Ответим в течение 1-2 часов.",
    "📦 Как сделать заказ": "Для заказа напишите нам в личные сообщения или нажмите кнопку 'Связаться'. Мы обсудим детали и приступим к работе.",
    "🔄 Гарантии и возврат": "Мы гарантируем качество работы. Если результат не устраивает — бесплатно доработаем. Возврат средств возможен до начала работы.",
    "📞 Контакты": "Telegram: @your_username\nEmail: your@email.com\nРаботаем по всему СНГ.",
}

CONTACT_USERNAME = "@your_username"  # Юзернейм для связи

logging.basicConfig(level=logging.INFO)



bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()


def get_main_keyboard():
    """Главное меню с кнопками FAQ"""
    builder = ReplyKeyboardBuilder()
    for question in FAQ.keys():
        builder.add(KeyboardButton(text=question))
    builder.add(KeyboardButton(text="📞 Связаться"))
    builder.adjust(2)  # 2 кнопки в ряд
    return builder.as_markup(resize_keyboard=True)


def get_contact_keyboard():
    """Инлайн-кнопка для связи"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="✍️ Написать нам",
        url=f"https://t.me/{CONTACT_USERNAME.lstrip('@')}"
    ))
    return builder.as_markup()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я помогу ответить на частые вопросы.\n"
        "Выбери тему из меню ниже 👇",
        reply_markup=get_main_keyboard()
    )


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "📋 Доступные команды:\n\n"
        "/start — Главное меню\n"
        "/faq — Список всех вопросов\n"
        "/contact — Связаться с нами"
    )


@dp.message(Command("faq"))
async def faq_list(message: types.Message):
    text = "📚 Часто задаваемые вопросы:\n\n"
    for i, question in enumerate(FAQ.keys(), 1):
        text += f"{i}. {question}\n"
    text += "\nНажми на кнопку в меню, чтобы получить ответ."
    await message.answer(text, reply_markup=get_main_keyboard())


@dp.message(Command("contact"))
async def contact_command(message: types.Message):
    await message.answer(
        "📞 Свяжитесь с нами:",
        reply_markup=get_contact_keyboard()
    )


@dp.message(F.text == "📞 Связаться")
async def contact_button(message: types.Message):
    await message.answer(
        "Мы рады помочь! Нажмите кнопку ниже 👇",
        reply_markup=get_contact_keyboard()
    )


@dp.message(F.text.in_(FAQ.keys()))
async def answer_faq(message: types.Message):
    answer = FAQ.get(message.text)
    await message.answer(
        f"{message.text}\n\n{answer}",
        reply_markup=get_main_keyboard()
    )


@dp.message()
async def unknown_message(message: types.Message):
    await message.answer(
        "🤔 Не понял вопрос. Используй кнопки меню или напиши /help",
        reply_markup=get_main_keyboard()
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
