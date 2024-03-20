import aiogram
import aiogram.filters as filters
import asyncio
import modules.settings as m_set

admin_button = aiogram.types.KeyboardButton(text = "Адміністратор")
klient_button = aiogram.types.KeyboardButton(text = "Клієнт")

keyboard = aiogram.types.ReplyKeyboardMarkup(keyboard = [[klient_button, admin_button]], one_time_keyboard = True)

@m_set.dispatcher.message(filters.CommandStart())
async def bot_start(message: aiogram.types.Message):
    await message.answer(text = "Добрий день, оберіть Ваш статус, будь ласка.", reply_markup = keyboard)

async def main():
    await m_set.dispatcher.start_polling(m_set.bot)