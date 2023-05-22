from aiogram import Dispatcher,Bot,executor
from aiogram.types import Message
import requests
import logging

logging.basicConfig(level=logging.INFO)

bot=Bot(token="5897018152:AAHuJK5D2SWMLIqcT8qOTno3pMVyQ6AUunA")
dp=Dispatcher(bot)

@dp.message_handler(commands="start")
async def ob(message:Message):
    await message.reply("Assalomu Alaykum👐 \nOb havo🌡  malumotini bilish uchun Shahar nomini kiriting?")



@dp.message_handler()
async def obhavo(message:Message):
    
    shahar=message.text
    try:
        token="7311aa89429bc363d47d76b65ae85633"
        res=requests.get(f"https://api.openweathermap.org/data/2.5/weather?&q={shahar}&appid={token}")
        info=res.json()
        havo=int(info['main']['temp']-273)
        daraja=''
        if havo>=25:
            daraja="issiq"
        else:
            daraja='iliq'

        await message.reply(f" [ {shahar} ] \n\nOb-havo🌤: \n\nNamlik☀️ : +{havo, daraja} \nShamol tezligi💨 : {info['wind']['speed']} m/s ")
    except:
        await message.reply("Bunday joy topilmadi?")

if __name__=="__main__":
    executor.start_polling(dp,skip_updates=True)