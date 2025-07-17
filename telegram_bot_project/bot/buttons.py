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
    button_update = KeyboardButton(text=UPDATE_IDEA_BUTTON)
    button_delete = KeyboardButton(text=DEL_IDEA_BUTTON)
    button_add = KeyboardButton(text=BUTTON_IDEA)
    button_all_ideas = KeyboardButton(text=ALL_IDEAS)

    idea_reply_keyboard.keyboard.append([button_delete, button_add])
    idea_reply_keyboard.keyboard.append([button_update, button_all_ideas])
    idea_reply_keyboard.keyboard.append([button_menu])

    return idea_reply_keyboard

def task_reply_keyboard() -> InlineKeyboardMarkup:
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[], row_width=2)

    button_yes: InlineKeyboardButton = InlineKeyboardButton(text=BUTTON_YES, callback_data="yes_task")
    button_no: InlineKeyboardButton = InlineKeyboardButton(text=BUTTON_NO, callback_data="no_task")

    inline_markup.inline_keyboard.append([button_yes, button_no])
    return inline_markup

def task_menu_keyboard() -> ReplyKeyboardMarkup:
    task_menu_keyboard = ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True, row_width=2)

    button_menu = KeyboardButton(text=MENU_BUTTON)
    button_add = KeyboardButton(text=BUTTON_ADD_TASK)
    button_status = KeyboardButton(text=BUTTON_TOGGLE_STATUS)
    button_delete = KeyboardButton(text=BUTTON_DELETE_TASK)
    button_update = KeyboardButton(text=BUTTON_EDIT_TASK)
    button_all_tasks = KeyboardButton(text=BUTTON_ALL_TASKS)

    task_menu_keyboard.keyboard.append([button_add, button_status])
    task_menu_keyboard.keyboard.append([button_delete, button_update])
    task_menu_keyboard.keyboard.append([button_menu, button_all_tasks])

    return task_menu_keyboard