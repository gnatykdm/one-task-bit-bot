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
    menu_reply_keyboard = ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True, row_width=2)

    button_settings = KeyboardButton(text=BUTTON_SETTINGS)
    button_idea = KeyboardButton(text=BUTTON_IDEA)
    button_day = KeyboardButton(text=BUTTON_MYDAY)
    button_task = KeyboardButton(text=BUTTON_ADD_TASK)

    menu_reply_keyboard.keyboard.append([button_settings, button_idea])
    menu_reply_keyboard.keyboard.append([button_day, button_task])

    return menu_reply_keyboard

def get_idea_conf_keyboard() -> InlineKeyboardMarkup:
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[], row_width=2)

    delete_button: InlineKeyboardButton = InlineKeyboardButton(text=DEL_BUTTON, callback_data="delete_idea")
    save_button: InlineKeyboardButton = InlineKeyboardButton(text=SAVE_BUTTON, callback_data="save_idea")

    inline_markup.inline_keyboard.append([delete_button, save_button])
    return inline_markup

def idea_reply_keyboard() -> ReplyKeyboardMarkup:
    idea_reply_keyboard = ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True, row_width=2)

    button_menu = KeyboardButton(text=MENU_BUTTON)
    button_delete = KeyboardButton(text=DEL_IDEA_BUTTON)
    button_add = KeyboardButton(text=BUTTON_IDEA)
    button_all_ideas = KeyboardButton(text=ALL_IDEAS)

    idea_reply_keyboard.keyboard.append([button_delete, button_add])
    idea_reply_keyboard.keyboard.append([button_menu, button_all_ideas])

    return idea_reply_keyboard