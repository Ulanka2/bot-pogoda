import os
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


config_dict = get_default_config()
config_dict['language'] = 'ru'  # your language here, eg. russia

owm = OWM('0c7983ae2b01c1268cf07cd074c8cc67', config_dict)
mgr = owm.weather_manager()
TELEGRAM_TOKEN =  os.environ.get('TELEGRAM_TOKEN')
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def first_or_help_commands(message: types.Message):
    await bot.send_message(message.from_user.id," Привет Друг! Напиши в каком ты Стране или В городе?")
    await bot.send_message(message.from_user.id," И я тебе скажу какая сейчас погодка! ")

@dp.message_handler(content_types=["text"])
async def echo_message(message: types.Message):
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temp = w.temperature('celsius')["temp"]
        answer = "В городе " + message.text + " Сегодня " +  w.detailed_status + " ! " + "\n\n"
        answer += "Температура сейчас в районе " + str(temp) + " \n\n"
        if temp < 10:
            answer += "Сейчас ппц как холодно, одевайся как танк :D) " + "\n"
        elif temp < 15:
            answer += "Сейчас холодно, одевайся потеплее."
        else:
            answer += "Температура норм, одевай что угодно."
        await bot.send_message(message.from_user.id, answer)


if __name__ == '__main__':
    executor.start_polling(dp)