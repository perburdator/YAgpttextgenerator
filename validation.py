import telebot
from telebot import types

from other import *
from sqlite3forgpt import get_dialogue_for_user, get_value_from_table, is_value_in_table
from keyboard import create_keyboard


def get_user_session_id(user_id: int) -> int:
    row = get_value_from_table(db_name, 'session_id', user_id)
    return row['session_id']


def send_session_limit_warning(bot: telebot.TeleBot, user_id: int, session_id: int):
    if session_id >= (MAX_SESSIONS // 2):
        bot.send_message(user_id, f'u are getting barelly sessions number {session_id}'
                                  f'amount of all sessions {MAX_SESSIONS}')


def send_session_limit_ended_message(bot: telebot.TeleBot, user_id: int):
    bot.send_message(user_id, 'u ended all ur sessions sorry so u can watch logs by this command',
                     reply_markup=create_keyboard(['/debug']))


def is_session_limit(message: types.Message, bot: telebot.TeleBot) -> bool:
    user_id = message.from_user.id
    if not is_value_in_table(db_name, 'user_id', user_id):
        return False

    session_id = get_user_session_id(user_id)

    if session_id >= MAX_SESSIONS:
        send_session_limit_ended_message(bot, message.chat.id)
        return True

    send_session_limit_warning(bot, message.chat.id, session_id)
    return False


def get_total_tokens_in_session(user_id: int) -> int:
    row = get_value_from_table(db_name, 'session_id', user_id)
    session = get_dialogue_for_user(user_id, row['session_id'])
    tokens_in_session = 0
    for rec in session:
        tokens_in_session += rec['tokens']
    return tokens_in_session


def send_token_limit_warning(bot: telebot.TeleBot, chat_id: int, all_tokens: int):
    bot.send_message(chat_id, f'Вы приближаетесь к минимуму токенов от максимума {MAX_TOKENS_IN_SESSION}'
                              f'Ваш запрос составил столько токенов {all_tokens}')


def send_all_tokens_are_end(bot: telebot.TeleBot, chat_id: int):
    bot.send_message(chat_id, f'Вы израсходовали все токены в этой сессии'
                              f'Но вы можете посмотреть список других команд',
                     reply_markup=create_keyboard(HELP_COMMANDS))


def is_token_limit(message: types.Message, message_tokens: int, bot: telebot.TeleBot) -> bool:
    user_id = message.from_user.id
    all_tokens = message_tokens + get_total_tokens_in_session(user_id)

    if all_tokens >= MAX_TOKENS_IN_SESSION:
        send_all_tokens_are_end(bot, message.chat.id)
        return True

    elif all_tokens >= (MAX_TOKENS_IN_SESSION // 2):
        send_token_limit_warning(bot, message.chat.id, all_tokens)
        return False

    return False
