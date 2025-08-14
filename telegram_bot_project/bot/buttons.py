# bot/buttons.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from messages import *
from typing import Optional, List

def get_language_keyboard() -> InlineKeyboardMarkup:
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[], row_width=2)

    button_ua: InlineKeyboardButton = InlineKeyboardButton(text=BUTTON_UA_LANG, callback_data="lang_ua")
    button_en: InlineKeyboardButton = InlineKeyboardButton(text=BUTTON_EN_LANG, callback_data="lang_en")

    inline_markup.inline_keyboard.append([button_ua, button_en])

    return inline_markup

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

    button_yes: InlineKeyboardButton = InlineKeyboardButton(text=BUTTON_YES_BTN, callback_data="yes_task")
    button_no: InlineKeyboardButton = InlineKeyboardButton(text=BUTTON_NO_BTN, callback_data="no_task")

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

def settings_menu_keyboard() -> ReplyKeyboardMarkup:
    settings_menu_keyboard = ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True, row_width=2)

    main_menu_button = KeyboardButton(text=MENU_BUTTON)
    feedback_button = KeyboardButton(text=SETTINGS_BUTTON_FEEDBACK)
    language_button = KeyboardButton(text=SETTINGS_BUTTON_LANGUAGE)
    routine_button = KeyboardButton(text=SETTINGS_BUTTON_ROUTINE)
    routine_time = KeyboardButton(text=SETTINGS_BUTTON_ROUTINE_TIME)

    settings_menu_keyboard.keyboard.append([routine_time, routine_button])
    settings_menu_keyboard.keyboard.append([language_button, feedback_button])
    settings_menu_keyboard.keyboard.append([main_menu_button])

    return settings_menu_keyboard

def routine_time_keyboard() -> ReplyKeyboardMarkup:
    routine_time_keyboard = ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True, row_width=2)

    wake_time_button = KeyboardButton(text=ROUTINE_SET_WAKE_BUTTON)
    sleep_time_button = KeyboardButton(text=ROUTINE_SET_SLEEP_BUTTON)
    my_routine_button = KeyboardButton(text=ROUTINE_MY_TIME)
    settings_menu_button = KeyboardButton(text=BUTTON_SETTINGS)

    routine_time_keyboard.keyboard.append([wake_time_button, sleep_time_button])
    routine_time_keyboard.keyboard.append([my_routine_button, settings_menu_button])

    return routine_time_keyboard

def routine_menu_keyboard() -> InlineKeyboardMarkup:
    routine_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[], row_width=2)

    morning_routine_btn: InlineKeyboardButton = InlineKeyboardButton(text=ROUTINE_MORNING_VIEW, callback_data="morning_view")
    evening_routine_btn: InlineKeyboardButton = InlineKeyboardButton(text=ROUTINE_EVENING_VIEW, callback_data="evening_view")

    routine_markup.inline_keyboard.append([morning_routine_btn, evening_routine_btn])

    return routine_markup

def morning_routine_keyboard() -> ReplyKeyboardMarkup:
    add_btn = KeyboardButton(text=MORNING_ROUTINE_ADD_BTN)
    edit_btn = KeyboardButton(text=MORNING_ROUTINE_EDIT_BTN)
    drop_btn = KeyboardButton(text=MORNING_ROUTINE_DELETE_BTN)
    all_btn = KeyboardButton(text=MY_MORNING_ROUTINE_BTN)
    settings_btn = KeyboardButton(text=BUTTON_SETTINGS)
    evening_switch_btn = KeyboardButton(text=ROUTINE_EVENING_VIEW)

    keyboard: List[List[KeyboardButton]] = [
        [add_btn, edit_btn],
        [drop_btn, all_btn],
        [evening_switch_btn],
        [settings_btn]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        row_width=2
    )


def evening_routine_keyboard() -> ReplyKeyboardMarkup:
    add_btn = KeyboardButton(text=EVENING_ROUTINE_ADD_BTN)
    edit_btn = KeyboardButton(text=EVENING_ROUTINE_EDIT_BTN)
    drop_btn = KeyboardButton(text=EVENING_ROUTINE_DELETE_BTN)
    all_btn = KeyboardButton(text=MY_EVENING_ROUTINE_BTN)
    settings_btn = KeyboardButton(text=BUTTON_SETTINGS)
    morning_switch_btn = KeyboardButton(text=ROUTINE_MORNING_VIEW)

    keyboard = [
        [add_btn, edit_btn],
        [drop_btn, all_btn],
        [morning_switch_btn],
        [settings_btn]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        row_width=2
    )

def focus_menu_keyboard(started: Optional[bool] = False) -> ReplyKeyboardMarkup:
    menu_btn = KeyboardButton(text=MENU_BUTTON)
    focus_btn = KeyboardButton(text=FOCUS_ZONE_END if started else FOCUS_ZONE_START)
    focus_list = KeyboardButton(text=ALL_FOCUSES_BTN)
    delete_focus = KeyboardButton(text=DELETE_FOCUS)

    keyboard = [
        [focus_btn],
        [focus_list],
        [delete_focus],
        [menu_btn]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def focus_save_question_keyboard() -> InlineKeyboardMarkup:
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[], row_width=2)

    save_focus_btn = InlineKeyboardButton(text=FOCUS_INLINE_YES, callback_data="save_focus")
    not_save_focus_btn = InlineKeyboardButton(text=FOCUS_INLINE_NO, callback_data="not_save_focus")

    inline_markup.inline_keyboard.append([save_focus_btn, not_save_focus_btn])

    return inline_markup


def focus_title_ask_keyboard() -> InlineKeyboardMarkup:
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[], row_width=2)

    add_title = InlineKeyboardButton(text=FOCUS_INLINE_YES, callback_data="add_title")
    not_add_title = InlineKeyboardButton(text=FOCUS_INLINE_NO, callback_data="not_add_title")

    inline_markup.inline_keyboard.append([add_title, not_add_title])

    return inline_markup

def work_buttons_keyboard(task_id: int) -> InlineKeyboardMarkup:
    inline_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[], row_width=2)

    start_work_btn: InlineKeyboardButton = InlineKeyboardButton(text=START_WORK_BTN, callback_data=f"complete_task:{task_id}")
    cancel_work_btn: InlineKeyboardButton = InlineKeyboardButton(text=CANCEL_WORK_BTN, callback_data=f"cancel_task:{task_id}")

    inline_markup.inline_keyboard.append([start_work_btn, cancel_work_btn])
    return inline_markup

def get_work_session_keyboard() -> None:
    task_finished = KeyboardButton(text=STOP_WORK_SESSION)
    task_break = KeyboardButton(text=CANCEL_WORK_BTN)

    keyboard = [
        [task_break, task_finished]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def get_start_day_btn() -> ReplyKeyboardMarkup:
    start_day_btn = KeyboardButton(text=START_DAY_BTN)

    keyboard = [
        [start_day_btn]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )