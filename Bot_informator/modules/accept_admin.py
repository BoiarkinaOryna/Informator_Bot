import aiogram
import asyncio
import modules.settings as m_set
import modules.create_telebot as m_create_telebot
import modules.write_data_base as m_db
# import modules.creatre_message as m_message

moderator_id = "1458244679"

button_accept = aiogram.types.InlineKeyboardButton(text = 'Схвалити', callback_data = 'Схвалено')
button_decline = aiogram.types.InlineKeyboardButton(text = 'Відмовити', callback_data = 'Відмовлено')

inline_keyboard = aiogram.types.InlineKeyboardMarkup(inline_keyboard = [[button_accept, button_decline]])

async def accept_admin():
   global moderator_id 
   await m_set.bot.send_message(chat_id = moderator_id, text = f"Схваліть, будь ласка, адміністратора {moderator_id}", reply_markup = inline_keyboard)
   
@m_set.dispatcher.callback_query(aiogram.F.data == "Схвалено")
# async def new_admin(callback: aiogram.types.CallbackQuery, message: aiogram.types.Message):
async def new_admin(message: aiogram.types.Message):
   length = len(m_set.admins)
   length += 1 
   print(length)
   key = f"admin{str(length)}"
   m_set.admins[key] = m_set.admin_data
   print(
      "admins =", m_set.admins, "\n",
      "admin_data =", m_set.admin_data
      )
   m_db.write_data(table = 'Administrators', my_email = m_set.admins[key]["email"], my_nick = m_set.admins[key]["name"], my_number = m_set.admins[key]["phone_number"], my_password = m_set.admins[key]["password"])
   m_set.admin_data = []