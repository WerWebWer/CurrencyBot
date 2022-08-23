# -*- coding: utf8 -*- 

import telebot
from telebot import types
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import logging

import config
import db
from utils import isfloat
from utils import log
from utils import log_for_buttons
from utils import log_bot

bot=telebot.TeleBot(config.BOT_TOKEN)

# Клавиатура под полем ввода
keyboard_currencies=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_currencies.row('RUB', 'USD', 'EUR')
keyboard_currencies.add('AMD', 'HUF', 'RUB')

# Клавиатура под сообщением
buttons_menu = [[types.InlineKeyboardButton(text="RUB", callback_data="rub"), types.InlineKeyboardButton(text="USD", callback_data="usd"), types.InlineKeyboardButton(text="EUR", callback_data="eur")],
    [types.InlineKeyboardButton(text="AMD", callback_data="amd"),types.InlineKeyboardButton(text="HUF", callback_data="huf"), types.InlineKeyboardButton(text="RSD", callback_data="rsd")]]
button_currencies = types.InlineKeyboardMarkup(buttons_menu)

def convert(message):
    money = message.text
    if isfloat(money):
        money = float(money)
        def_cur = db.db_get_cur(message.chat.id)
        data = requests.get('https://api.exchangerate-api.com/v4/latest/' + def_cur).json()
        rates = data["rates"]

        rub = float(rates["RUB"])
        usd = float(rates["USD"])
        eur = float(rates["EUR"])
        amd = float(rates["AMD"])
        huf = float(rates["HUF"])
        rsd = float(rates["RSD"])

        msg = 'Получено: ' + str(money) + ' ' + def_cur + '\n\n'
        msg += 'RUB - <b>' + str(round(money*rub, 2)) + '₽</b>\n'
        msg += 'USD - <b>' + str(round(money*usd, 2)) + '$</b>\n'
        msg += 'EUR - <b>' + str(round(money*eur, 2)) + '€</b>\n'
        msg += 'AMD - <b>' + str(round(money*amd, 2)) + '֏</b>\n'
        msg += 'HUF - <b>' + str(round(money*huf, 2)) + 'ƒ</b>\n'
        msg += 'RSD - <b>' + str(round(money*rsd, 2)) + 'din</b>\n'

        log_bot(message, "Return currency")
        return msg
    else:
        log_bot(message, "Not number")
        return 'Это не число\nПросьба написать число'

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    log(m, m.text)
    bot.send_message(m.chat.id, 'Я на связи. Готов')
    bot.send_message(m.chat.id, 'Выберите валюту, в которой будете вводить по умолчанию\n' + 
        'После, отправляйте мне сумму и я буду её переводить\n\n' +
        'Для помощи вызовите /help', reply_markup=button_currencies)
    db.db_add_new(m.chat.id, 'RUB')

# Функция, обрабатывающая команду /currency
@bot.message_handler(commands=["currency"])
def start(message, res=False):
    log(message, message.text)
    bot.send_message(message.chat.id, "Пожалуйста выберите следующую вводимую по умолчанию валюту", reply_markup=button_currencies)

@bot.message_handler(commands=['help'])
def help_message(message):
    log(message, message.text)
    bot.send_message(message.chat.id, 'Бот, который конвертирует валюту по курсу на день\n\n' + 
        'Доступны: <b>RUB, USD, EUR, AMD, HUF, RSD</b>\n\n' +
        '/start - переззапустить бота'+
        '/help - вывести данное сообщение\n' + 
        '/currency - поменять вводимую по умолчанию валюту', parse_mode='HTML')

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    log(message, message.text)
    bot.send_message(message.chat.id, convert(message), parse_mode='HTML')
    log_bot(message, "Send message")

@bot.message_handler(content_types=['sticker', 'audio', 'document', 'video', 'video_note', 'voice', 'location', 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'])
def other_msg(message):
    log(message, message.text)
    help_message(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    id = call.message.chat.id
    id_msg = call.message.message_id
    cur ="RUB"
    if call.message:
        if call.data == "rub":
            cur="RUB"
        elif call.data == "usd":
            cur="USD"
        elif call.data == "eur":
            cur="EUR"
        elif call.data == "amd":
            cur="AMD"
        elif call.data == "huf":
            cur="HUF"
        elif call.data == "rsd":
            cur="RSD"

        bot.send_message(id, 'Выбрано по умолчанию ' + cur, reply_to_message_id=id_msg)
        db.db_update_value(id, cur)
        log_for_buttons(id, call, "Choose " + cur)

    # Если сообщение из инлайн-режима
    # НО! Это не включено -> не работает
    elif call.inline_message_id:
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")

db.db_connect()

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Перезапуск бота"),
    telebot.types.BotCommand("/help", "Помощь"),
    telebot.types.BotCommand("/currency", "Изменить валюту по умолчанию")
])
try:
    bot.polling(none_stop=True, interval=0)
except error:
    telebot.TeleBot(config.BOT_TOKEN).send_message(config.ID_ADMIN, "Bot down")
    print("BOT DOWN")
