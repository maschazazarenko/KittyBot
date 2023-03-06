"""
Файл предназначен для работы телеграм бота по выдаче картинок котиков и собак.
"""

import logging
import os

import requests

from dotenv import load_dotenv

from telegram.ext import CommandHandler, Updater
from telegram import ReplyKeyboardMarkup

# Подключены логи. Ошибки выводятся в файл program.log.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='program.log',
    encoding='utf-8',
    filemode='w',
)

# Функция для импорта переменной токена.
load_dotenv()
secret_token = os.getenv('TOKEN')
# Указываем токен из переменной в программу обработчика.
updater = Updater(token=secret_token)
# API адреса используемые в работе программы.
URL = 'https://api.thecatapi.com/v1/images/search'
URL_2 = 'https://api.thedogapi.com/v1/images/search'


def get_new_image_cat():
    """
    Функция для получения картинок кошек с сервиса API.
    Если возникает ошибка в работе API сервиса, то обрщаемся
    к сервису с картинками собак.
    """
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = URL_2
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def get_new_image_dog():
    """
    Функция для получения картинок собак с сервиса API.
    Если возникает ошибка в работе API сервиса, то обрщаемся
    к сервису с картинками котиков.
    """
    try:
        response = requests.get(URL_2)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = URL
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    """Функция для вывода картинок кошек в чат бота."""
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image_cat())


def new_dog(update, context):
    """Функция для вывода картинок собак в чат бота."""
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image_dog())


def wake_up(update, context):
    """
    Начальная функция, после команды /start.
    В этой функции мы обозначим кнопки для запроса картинок.
    При первом обращении к боту, приветствует человека по имени,
    а после выводит картинку котика.
    """
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat', '/newdog']],
                                 resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Лови котика!'.format(name),
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image_cat())


def main():
    """Укажем обработчики, которые будут работать только в этом файле."""
    updater = Updater(token=secret_token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('newdog', new_dog))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
