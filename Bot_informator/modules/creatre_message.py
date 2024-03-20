import aiogram
import requests
import os
import asyncio
import modules.settings as m_set
import modules.get_chat_id as m_id
import modules.registration as m_registration

button_confirm = aiogram.types.InlineKeyboardButton(text = "Підтвердити", callback_data = "Підтвердити")
button_choose = aiogram.types.InlineKeyboardButton(text = "Обрати", callback_data = "Обрати")
button_info = aiogram.types.InlineKeyboardButton(text = "Інформація", callback_data = "Інфо")
inline_keyboard = aiogram.types.InlineKeyboardMarkup(inline_keyboard = [[button_confirm, button_choose, button_info]])

file_id = None
flag_info = None
flag_photo = False
info = None

@m_set.dispatcher.message(m_registration.Reg_admin.idle_a)
async def create_message(message: aiogram.types.Message):
    global flag_photo
    print("get_photo create_message")
    if flag_photo == False:
        await get_photo(message1 = message)
        flag_photo = True
    await get_information(message1 = message)

async def get_photo(message1: aiogram.types.Message):
    global file_id
    print("get_photo")
    print("message.photo =", message1.photo)
    # await message.reply(message.photo[-1].file_id)
    file_id = message1.photo[-1].file_id
    print(file_id)

async def get_information(message1: aiogram.types.Message):
    global flag_info, info
    # texting = True
    # while texting == True:
    print("message.text =", message1.text)
    if flag_info == None:
        await message1.answer(text = "Введіть інформацію про товар\n Першим рядком введіть назву товару і поставте ': \n Наприклад: 'Корм Brit:'")
        flag_info = "info"
    elif flag_info == "info" and message1.text != None:
        # texting = False
        info = message1.text
        await message1.answer(text = f"Інформацію додано: {info}")
        list_id = m_id.get_all_id()
        print(list_id)
        for id in list_id:
            await m_set.bot.send_photo(chat_id = id[0], photo = file_id, reply_markup = inline_keyboard)
@m_set.dispatcher.callback_query(aiogram.F.data == 'Інфо')
async def get_info(callback: aiogram.types.CallbackQuery):
    await callback.message.answer(text = info)
