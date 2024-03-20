import aiogram
import aiogram.filters as filters
import aiogram.fsm.state as aiogram_state
import asyncio


import modules.settings as m_set
import modules.write_data_base as m_db
import modules.accept_admin as m_accept
# import modules.creatre_message as m_message
import modules.get_chat_id as m_get_chat_id 

button_reg_a = aiogram.types.KeyboardButton(text = "Зареєструватися як адмін")
button_author_a = aiogram.types.KeyboardButton(text = "Авторизуватися як адмін")
keyboard_a = aiogram.types.ReplyKeyboardMarkup(keyboard = [[button_reg_a, button_author_a]])

button_reg_c = aiogram.types.KeyboardButton(text = "Зареєструватися як клієнт")
button_author_c = aiogram.types.KeyboardButton(text = "Авторизуватися як клієнт")
keyboard_c = aiogram.types.ReplyKeyboardMarkup(keyboard = [[button_reg_c, button_author_c]])


router = aiogram.Router()
m_set.dispatcher.include_router(router)
waiting_messages = {}

class Reg_client(aiogram_state.StatesGroup):
    idle_c = aiogram_state.State()
    email_c = aiogram_state.State()
    nick_c = aiogram_state.State()
    phone_number_c = aiogram_state.State()
class Reg_admin(aiogram_state.StatesGroup):
    idle_a = aiogram_state.State()
    email_a = aiogram_state.State()
    nick_a = aiogram_state.State()
    password = aiogram_state.State()
    phone_number_a = aiogram_state.State()
   
   
@router.message(aiogram.F.text == "Адміністратор")
async def admin_registration(message: aiogram.types.Message):
    global email_a, nick_a, password, phone_number_a
    #if message.text == "Адміністратор":
    print("admin_reg")
    print("aiogram.F.text =", aiogram.F.text)
    await message.answer(text = "Зареєструйтесь, або виберіть авторизацію, якщо ви вже зареєстровані.", reply_markup = keyboard_a)
        
@router.message(aiogram.F.text == "Зареєструватися як адмін") 
# (message: aiogram.types.Message):
async def registration_a(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    print("state in admin =", state)
    await message.answer(text = 'Створіть свій нікнейм')
    await state.set_state(Reg_admin.nick_a)

@router.message(Reg_admin.nick_a)
async def get_admin_nick(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    nick_admin = message.text
    await state.update_data(name = nick_admin)
    await message.answer(text = "Вигадайте надійний пароль")
    await state.set_state(Reg_admin.password)

@router.message(Reg_admin.password)
async def get_admin_password(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    password = message.text
    await state.update_data(password = password)
    await message.answer(text = "Введіть свій номер телефону")
    await state.set_state(Reg_admin.phone_number_a)

@router.message(Reg_admin.phone_number_a)
async def get_admin_phone(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    phone_number = message.text
    await state.update_data(phone_number = phone_number)
    await message.answer(text = "Введіть свій email ")
    await state.set_state(Reg_admin.email_a)

@router.message(Reg_admin.email_a)
async def get_admin_email(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    email_admin = message.text
    await state.update_data(email = email_admin)
    # await message.answer(text = "Реєстрацію завершено успішно")
    admin_data = await state.get_data()
    m_set.admin_data = admin_data
    print("admin data =", admin_data)
    # email = admin_data.get('email')
    # nick = admin_data.get('name')
    # phone_number = admin_data.get("phone_number")
    # password = admin_data.get('password')
    await m_accept.accept_admin()
    await state.set_state(Reg_admin.idle_a)
    # m_db.write_data(table = 'Administrators', my_email = email , my_nick = nick, my_number = phone_number, my_password = password, id = None)


@router.message(aiogram.F.text == "Клієнт")
async def client_registration(message: aiogram.types.Message):
    global email_a, nick_a, phone_number_a
    #if message.text == "Адміністратор":
    print("client_reg")
    print("aiogram.F.text =", aiogram.F.text)
    await message.answer(text = "Зареєструйтесь, або виберіть авторизацію, якщо ви вже зареєстровані.", reply_markup = keyboard_c)
        
@router.message(aiogram.F.text == "Зареєструватися як клієнт") 
# (message: aiogram.types.Message):
async def registration_c(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    all_id = m_get_chat_id.get_all_id()
    for id in all_id:
        print("id=", id, "\n message.chat.id=", message.chat.id )
        if int(id[0]) == message.chat.id:
            await message.answer("Ви вже зареєстровані. Будь ласка, виберіть авторизацію", reply_markup = keyboard_c)
            await state.set_state(Reg_client.idle_c)
            break
    else:   
        await message.answer(text = 'Створіть свій нікнейм:')
        await state.set_state(Reg_client.nick_c)


@router.message(Reg_client.nick_c)
async def get_client_nick(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    nick_client = message.text
    await state.update_data(name = nick_client)
    await message.answer(text = "Введіть свій номер телефону:")
    await state.set_state(Reg_client.phone_number_c)

@router.message(Reg_client.phone_number_c)
async def get_client_phone(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    phone_number = message.text
    await state.update_data(phone_number = phone_number)
    await message.answer(text = "Введіть свій email:")
    await state.set_state(Reg_client.email_c)

@router.message(Reg_client.email_c)
async def get_client_email(message: aiogram.types.Message, state: aiogram.fsm.context.FSMContext):
    if state != Reg_client.idle_c:
        email_client = message.text
        await state.update_data(email = email_client)
        await state.set_state(Reg_client.idle_c)
        await message.answer(text = "Реєстрацію завершено успішно")
        client_data = await state.get_data()
        email = client_data.get('email')
        nick = client_data.get('name')
        phone_number = client_data.get("phone_number")
        password = client_data.get('password')
        my_id = message.chat.id
        print("my_id = ", my_id)
        print(email, nick, phone_number, password)
        m_db.write_data(table = 'Clients', my_email = email , my_nick = nick, my_number = phone_number, my_password = password, id = my_id)