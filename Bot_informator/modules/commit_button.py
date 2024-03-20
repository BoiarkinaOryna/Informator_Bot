import aiogram
import asyncio
import modules.settings as m_set
import modules.creatre_message as m_message
import modules.change_choose_button as m_chnge_button
import sqlite3

async def write_data_product(name1, quantity1, customer_id1 , phone1: str, email1: str):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    phone1 = cursor.execute(f"SELECT phone_number FROM Clients WHERE id = {m_set.id}")
    print
    print("phone1 =", phone1)
    print("Data Base Product write")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS Products (id INTEGER PRIMARY KEY, name TEXT, quantity TEXT, customer_id TEXT, phone TEXT, email TEXT)")
    cursor.execute(f"INSERT INTO Products (id, name, quantity, customer_id, phone, email) VALUES (?, ?, ?, ?, ?, ?)", (m_set.id, name1, quantity1, customer_id1, str(phone1), str(email1)))
   
    m_set.id += 1
    connection.commit()
    connection.close()

@m_set.dispatcher.callback_query(aiogram.F.data == "Підтвердити")
async def commit_button(query: aiogram.types.CallbackQuery):
    product_name = m_message.info.split(":")[0]
    print("product_name =", product_name)
    print("message in commit_button =", query.message)
    if m_chnge_button.count == 0:
        query.message.answer(text="Оберіть кількість товарів \n наразі вона дорівнює 0.\n Щоб додати товари натисніть на кнопку 'Обрати")
    else:
        print("message_id=", query.message.chat.id)
        await write_data_product(name1 = product_name, quantity1 = m_chnge_button.count, customer_id1 = query.message.chat.id, phone1 = "dffcg", email1 = "fjjn")