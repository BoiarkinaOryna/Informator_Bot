import aiogram
import asyncio
# import modules.creatre_message as m_message
import modules.settings as m_set

count = 0

@m_set.dispatcher.callback_query(aiogram.F.data == "Обрати")
async def choose_button(callback: aiogram.types.CallbackQuery):
    global count
    print("choose button clicked")
    count += 1
    callback.message.reply_markup.inline_keyboard[0][1].text = f"Обрати: {count}"
    await callback.message.edit_reply_markup(
        inline_message_id = callback.inline_message_id,
        reply_markup = callback.message.reply_markup
    )