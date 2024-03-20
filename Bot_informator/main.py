import modules.create_telebot as create_bot
import asyncio
try:
  asyncio.run(create_bot.main())
except KeyboardInterrupt:
  print("Програма була припинена")