from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from messages import *


def get_language_keyboard() -> InlineKeyboardMarkup:
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[], row_width=2)

    button_ua: InlineKeyboardButton = InlineKeyboardButton(text=BUTTON_UA_LANG, callback_data="lang_ua")
    button_en: InlineKeyboardButton = InlineKeyboardButton(text=BUTTON_EN_LANG, callback_data="lang_en")

    inline_markup.inline_keyboard.append([button_ua, button_en])

    return inline_markup


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def menu_reply_keyboard() -> ReplyKeyboardMarkup:
    reply_keyboard = ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True, row_width=2)

    button_settings = KeyboardButton(text=BUTTON_SETTINGS)
    button_idea = KeyboardButton(text=BUTTON_IDEA)
    button_day = KeyboardButton(text=BUTTON_MYDAY)
    button_task = KeyboardButton(text=BUTTON_ADD_TASK)

    reply_keyboard.keyboard.append([button_settings, button_idea])
    reply_keyboard.keyboard.append([button_day, button_task])

    return reply_keyboard