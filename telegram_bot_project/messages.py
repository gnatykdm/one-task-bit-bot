from typing import Any
from aiogram import types, Bot
from service.user import UserService
from service.routine import RoutineService

MESSAGES: Any = {
    "UKRANIAN": {
        "START_MSG": (
            "🎉 Вітаємо! \n"
            "Готові розпочати роботу? Я допоможу організувати ваш день. 📋"
        ),
        "START_MSG_AGAIN": (
            "👋 Ви повернулися! \n"
            "Готові продовжити? Обирайте дію через /menu. 📌"
        ),
        "HELP_MSG": (
            "❓ Потрібна допомога? \n"
            "Використовуйте /start, /language або /menu для навігації. 📚"
        ),
        "MENU_MSG": (
            "📋 Ось ваше меню. \n"
            "Виберіть потрібну опцію для продовження. ⚙️"
        ),
        "AUTHORIZATION_PROBLEM": (
            "🚫 Виникла проблема з авторизацією. \n"
            "Спробуйте /start для початку. 🔄"
        ),
        "TEXT_RESPONSE": (
            "✉️ Отримано: \"{response}\". \n"
            "Дякуємо за ваш ввід! 📝"
        ),
        "CONTINUE_MSG": (
            "➡️ Що далі? \n"
            "Відкрийте /menu, щоб обрати наступну дію. 📋"
        ),
        "SETTINGS_RESPONSE": "⚙️ Відкриваємо налаштування. Давайте налаштуємо все під вас. 🔧",
        "MYDAY_RESPONSE": "📅 Ваш план на день готовий. Перегляньте його! 🕒",
        "IDEA_RESPONSE": "💡 Маєте ідею? Напишіть, я збережу її. 📝",
        "IDEA_SAVED": "✅ Ідею збережено. Дякуємо за внесок! 📚",
        "ADD_TASK_RESPONSE": "📝 Додаємо завдання. Вкажіть деталі. 🛠️",
        "IDEA_ACTION": "📌 Що зробити з цією ідеєю? Виберіть дію. ⚙️",
        "IDEA_DELETE": "🗑️ Ідею видалено. Готові до нових? 📝",
        "IDEA_PROBLEM": "⚠️ Помилка збереження ідеї. Спробуйте ще раз. 🔄",
        "IDEAS_SHOW": "💡 Ваші ідеї готові до перегляду. 📋",
        "IDEA_EXISTS": "⚠️ Така ідея вже існує. Спробуйте нову. 💡",
        "ERROR_SAVING_IDEA": "⚠️ Не вдалося зберегти ідею. Спробуйте пізніше. ⏳",
        "NO_IDEAS": "📝 Ідей поки немає. Додайте першу! 🚀",
        "DELETE_IDEA": "ℹ️ Вкажіть номер ідеї для видалення. 🗑️",
        "UPDATE_IDEA": "ℹ️ Вкажіть номер ідеї для оновлення. ✏️",
        "NOT_VALID_IDEA_NUM": "❌ Неправильний номер ідеї. Спробуйте ще раз. 🔢",
        "INVALID_IDEA_NUM": "❌ Номер ідеї некоректний. Перевірте ще раз. 🔍",
        "IDEA_DELETED": "🗑️ Ідея №{} '{}' видалена. Готові до нових завдань? 📝",
        "ASK_NEW_IDEA_TEXT": "✏️ Введіть новий текст для ідеї №{} '{}'. 📝",
        "IDEA_UPDATED": "✅ Ідея №{} оновлена. Відмінна робота! 📚",
        "TASK_ADD": "📝 Вкажіть назву завдання для додавання. 🛠️",
        "TASK_DEADLINE_ASK": "⏰ Додати дедлайн до завдання? Виберіть опцію. 🕒",
        "TASK_DEADLINE_YES": "🕒 Введіть час дедлайну (наприклад, 13:10). 📅",
        "TASK_DEADLINE_NO": "✅ Завдання збережено без дедлайну. 📝",
        "TASK_DEADLINE_INVALID": "❌ Некоректний формат часу. Спробуйте ще раз. ⏳",
        "TASK_SAVED": "✅ Завдання збережено. Продовжуйте! 📋",
        "TASK_MENU": "📂 Меню завдань. Усе під контролем. 🛠️",
        "NO_TASKS": "❌ Завдань поки немає. Додайте нове через /task. 🚀",
        "YOUR_TASKS": "📋 Список ваших завдань. Обирайте! 🛠️",
        "TASK_DELETE_MSG": "🗑️ Вкажіть номер завдання для видалення. 📝",
        "INVALID_TASK_NUM": "❌ Некоректний номер завдання. Спробуйте ще раз. 🔢",
        "TASK_DELETED": "✅ Завдання №{} '{}' видалено. 📝",
        "TASK_DELETE_PROBLEM": "⚠️ Помилка видалення завдання. Спробуйте пізніше. ⏳",
        "COMPLETE_TASK_MSG": "✅ Вкажіть номер завершеного завдання. 🏆",
        "COMPLETE_TASK_INVALID": "❌ Некоректний номер завдання. Спробуйте ще раз. 🔢",
        "COMPLETE_TASK_SUCCESS": "🏆 Завдання №{} '{}' виконано. Відмінно! 📝",
        "COMPLETE_TASK_PROBLEM": "⚠️ Помилка оновлення завдання. Спробуйте ще раз. 🔄",
        "UPDATE_TASK_MSG": "✏️ Вкажіть номер завдання для оновлення. 📝",
        "UPDATE_TASK_INVALID": "❌ Некоректний номер завдання. Спробуйте ще раз. 🔢",
        "UPDATE_TASK_SUCCESS": "✅ Завдання №{} оновлено. Гарна робота! 📝",
        "UPDATE_TASK_PROBLEM": "⚠️ Помилка оновлення завдання. Спробуйте пізніше. ⏳",
        "UPDATE_TASK_NAME_MSG": "📝 Введіть нову назву завдання. 🛠️",
        "UPDATE_TASK_NAME_INVALID": "❌ Некоректна назва завдання. Спробуйте ще раз. 🔢",
        "SETTINGS_MENU": "⚙️ Меню налаштувань. Налаштуйте все за вашим бажанням. 🔧",
        "ROUTINE_MENU_DAY": "🌅 Налаштувати ранковий чи вечірній розпорядок? 📅",
        "MORNING_ROUTINE": "☀️ Ваш ранковий розпорядок готовий. 📋",
        "EVENING_ROUTINE": "🌙 Ваш вечірній розпорядок готовий. 📋",
        "ROUTINES_INVALID": "❌ Помилка з розпорядками. Спробуйте ще раз. 🔄",
        "ADD_MORNING_ROUTINE": "📝 Введіть назву ранкового розпорядку. 🛠️",
        "INVALID_MORNING_ROUTINE": "❌ Некоректна назва. Спробуйте ще раз. 🔢",
        "ROUTINE_EXISTS": "⚠️ Розпорядок з такою назвою вже існує. Виберіть іншу. 📝",
        "ROUTINE_SAVED": "✅ Розпорядок «{}» збережено. 📝",
        "MORNING_ROUTINE_SHOW": "☀️ Ваші ранкові розпорядки. 📋",
        "EVENING_ROUTINE_SHOW": "🌙 Ваші вечірні розпорядки. 📋",
        "NO_MORNING_ROUTINE": "📝 Ранкових розпорядків немає. Додайте перший! 🚀",
        "PROVIDE_ROUTINE_ID": "🔢 Вкажіть номер розпорядку для дії. 📝",
        "ROUTINE_DELETED": "🗑️ Розпорядок видалено. Готові до нових? 📝",
        "NEW_ROUTINE_NAME": "✏️ Введіть нову назву розпорядку. 📝",
        "ROUTINE_NAME_SET": "✅ Назва розпорядку змінена на «{}». 📝",
        "SMTP_MESSAGE_TEXT": "📝 Напишіть ваш відгук. Ми цінуємо вашу думку! 💬",
        "SMTP_MESSAGE_SENT": "🙏 Відгук отримано. Дякуємо за ваш внесок! 📝",
        "INVALID_MESSAGE": "❌ Некоректний текст. Спробуйте ще раз. 🔢",
        "SET_TIME_MSG": "⏰ Введіть час для таймера (наприклад, 10:00). 🕒",
        "TIMER_SET": "✅ Таймер встановлено на {}. 📅",
        "ROUTINE_TIME": "⏰ Прокидання о {}, сон о {}, тривалість дня: {}. 📋",
        "TIMER_INVALID": "❌ Некоректний формат часу (потрібно 10:00). Спробуйте ще раз. ⏳",
        "IDEA_EXIST": "⚠️ Ідея з такою назвою вже є. Виберіть іншу. 💡",
        "SEND_MORNING_MSG": "Доброго ранку, {}! ☀️",
        "SEND_EVENING_MSG": "Доброго вечора, {}! 🌙",
        "WELCOME_TO_FOCUS": "Вітаємо у зоні фокусу! 🎯",
        "START_FOCUS_MSG": "Сесію фокусу розпочато. 🕒",
        "STOP_FOCUS_MSG": "Сесію фокусу зупинено.\nТривалість: - {}хв {}с. ⏳",
        "SAVE_FOCUS_ZONE": "Зберегти сесію фокусу? 📝",
        "SAVED_FOCUS_MSG": "Сесію фокусу збережено. ✅",
        "NOT_SAVED_FOCUS_MSG": "Сесію фокусу не збережено. ❌",
        "TITLE_FOCUS_ZONE_MSG": "Бажаєте дати назву цій сесії? 📝",
        "NOT_FOUND_FOCUS_SESSION": "❗ Не знайдено початку фокус-сесії.",
        "FOCUS_INVALID": "❗ Неправильний параметр фокусування",
        "FOCUS_TITLE_ASK": "Будь ласка, введіть назву фокус-сесії.",
        "FOCUS_EXISTS": "❗ Фокус-сесія вже активна.",
        "FOCUS_LIST_TITLE": "🧠 Список ваших фокус-сесій",
        "NO_FOCUS_SESSIONS": "😕 У вас ще немає жодної фокус-сесії.",
        "LANGUAGE_ASK": (
            "🌐 Виберіть мову для роботи. \n"
            "Оберіть опцію нижче. 📚"
        ),
        "LANGUAGE_OK": "✅ Мову змінено. Готові продовжити? 🚀",
        "LANGUAGE_INVALID": "❌ Некоректний вибір мови. Спробуйте ще раз. 🔢",
        "DELETE_FOCUS_SESSION_MSG": "Вкажіть номер сесії, яку ви хочете видалити.",
        "FOCUS_DELETED": "✅ Фокус-сесію №{} з назвою \"{}\" успішно видалено.",
    },
    "ENGLISH": {
        "START_MSG": (
            "🎉 Welcome! \n"
            "Ready to start your day? I’m here to help you stay organized. 📋"
        ),
        "START_MSG_AGAIN": (
            "👋 You’re back! \n"
            "Ready to continue? Use /menu to choose an action. 📌"
        ),
        "HELP_MSG": (
            "❓ Need assistance? \n"
            "Try /start, /language, or /menu to navigate. 📚"
        ),
        "MENU_MSG": (
            "📋 Your menu is ready. \n"
            "Select an option to proceed. ⚙️"
        ),
        "AUTHORIZATION_PROBLEM": (
            "🚫 Authorization issue detected. \n"
            "Try /start to begin. 🔄"
        ),
        "TEXT_RESPONSE": (
            "✉️ Received: \"{response}\". \n"
            "Thank you for your input! 📝"
        ),
        "CONTINUE_MSG": (
            "➡️ What’s next? \n"
            "Open /menu to select your next action. 📋"
        ),
        "SETTINGS_RESPONSE": "⚙️ Accessing settings. Let’s customize your experience. 🔧",
        "MYDAY_RESPONSE": "📅 Your daily plan is ready. Review it now! 🕒",
        "IDEA_RESPONSE": "💡 Have an idea? Write it down, and I’ll save it. 📝",
        "IDEA_SAVED": "✅ Idea saved. Thank you for sharing! 📚",
        "ADD_TASK_RESPONSE": "📝 Adding a task. Provide the details. 🛠️",
        "IDEA_ACTION": "📌 What would you like to do with this idea? Select an action. ⚙️",
        "IDEA_DELETE": "🗑️ Idea deleted. Ready for new ones? 📝",
        "IDEA_PROBLEM": "⚠️ Error saving the idea. Please try again. 🔄",
        "IDEAS_SHOW": "💡 Your ideas are ready to view. 📋",
        "IDEA_EXISTS": "⚠️ This idea already exists. Try a new one. 💡",
        "ERROR_SAVING_IDEA": "⚠️ Failed to save the idea. Try again later. ⏳",
        "NO_IDEAS": "📝 No ideas yet. Add your first one! 🚀",
        "DELETE_IDEA": "ℹ️ Specify the idea number to delete. 🗑️",
        "UPDATE_IDEA": "ℹ️ Specify the idea number to update. ✏️",
        "NOT_VALID_IDEA_NUM": "❌ Invalid idea number. Try again. 🔢",
        "INVALID_IDEA_NUM": "❌ Incorrect idea number. Please check again. 🔍",
        "IDEA_DELETED": "🗑️ Idea #{} '{}' deleted. Ready for new tasks? 📝",
        "ASK_NEW_IDEA_TEXT": "✏️ Enter new text for idea #{} '{}'. 📝",
        "IDEA_UPDATED": "✅ Idea #{} updated. Great work! 📚",
        "TASK_ADD": "📝 Enter the task name to add. 🛠️",
        "TASK_DEADLINE_ASK": "⏰ Add a deadline for this task? Choose an option. 🕒",
        "TASK_DEADLINE_YES": "🕒 Enter the deadline time (e.g., 13:10). 📅",
        "TASK_DEADLINE_NO": "✅ Task saved without a deadline. 📝",
        "TASK_DEADLINE_INVALID": "❌ Invalid time format. Try again. ⏳",
        "TASK_SAVED": "✅ Task saved. Keep it up! 📋",
        "TASK_MENU": "📂 Task menu. Everything is under control. 🛠️",
        "NO_TASKS": "❌ No tasks yet. Add one with /task. 🚀",
        "YOUR_TASKS": "📋 List of your tasks. Choose one! 🛠️",
        "TASK_DELETE_MSG": "🗑️ Specify the task number to delete. 📝",
        "INVALID_TASK_NUM": "❌ Incorrect task number. Try again. 🔢",
        "TASK_DELETED": "✅ Task #{} '{}' deleted. 📝",
        "TASK_DELETE_PROBLEM": "⚠️ Error deleting task. Try again later. ⏳",
        "COMPLETE_TASK_MSG": "✅ Specify the completed task number. 🏆",
        "COMPLETE_TASK_INVALID": "❌ Incorrect task number. Try again. 🔢",
        "COMPLETE_TASK_SUCCESS": "🏆 Task #{} '{}' completed. Well done! 📝",
        "COMPLETE_TASK_PROBLEM": "⚠️ Error updating task. Try again. 🔄",
        "UPDATE_TASK_MSG": "✏️ Specify the task number to update. 📝",
        "UPDATE_TASK_INVALID": "❌ Incorrect task number. Try again. 🔢",
        "UPDATE_TASK_SUCCESS": "✅ Task #{} updated. Nice job! 📝",
        "UPDATE_TASK_PROBLEM": "⚠️ Error updating task. Try again later. ⏳",
        "UPDATE_TASK_NAME_MSG": "📝 Enter the new task name. 🛠️",
        "UPDATE_TASK_NAME_INVALID": "❌ Invalid task name. Try again. 🔢",
        "SETTINGS_MENU": "⚙️ Settings menu. Customize as needed. 🔧",
        "ROUTINE_MENU_DAY": "🌅 Set up a morning or evening routine? 📅",
        "MORNING_ROUTINE": "☀️ Your morning routine is ready. 📋",
        "EVENING_ROUTINE": "🌙 Your evening routine is ready. 📋",
        "ROUTINES_INVALID": "❌ Error with routines. Try again. 🔄",
        "ADD_MORNING_ROUTINE": "📝 Enter a title for your morning routine. 🛠️",
        "INVALID_MORNING_ROUTINE": "❌ Invalid title. Try again. 🔢",
        "ROUTINE_EXISTS": "⚠️ Routine with this title already exists. Choose another. 📝",
        "ROUTINE_SAVED": "✅ Routine «{}» saved. 📝",
        "MORNING_ROUTINE_SHOW": "☀️ Your morning routines. 📋",
        "EVENING_ROUTINE_SHOW": "🌙 Your evening routines. 📋",
        "NO_MORNING_ROUTINE": "📝 No morning routines yet. Add one! 🚀",
        "PROVIDE_ROUTINE_ID": "🔢 Specify the routine number for action. 📝",
        "ROUTINE_DELETED": "🗑️ Routine deleted. Ready for new plans? 📝",
        "NEW_ROUTINE_NAME": "✏️ Enter a new name for the routine. 📝",
        "ROUTINE_NAME_SET": "✅ Routine name changed to «{}». 📝",
        "SMTP_MESSAGE_TEXT": "📝 Share your feedback. We value your input! 💬",
        "SMTP_MESSAGE_SENT": "🙏 Feedback received. Thank you! 📝",
        "INVALID_MESSAGE": "❌ Invalid text. Try again. 🔢",
        "SET_TIME_MSG": "⏰ Enter the timer time (e.g., 10:00). 🕒",
        "TIMER_SET": "✅ Timer set for {}. 📅",
        "TIMER_INVALID": "❌ Invalid time format (use 10:00). Try again. ⏳",
        "ROUTINE_TIME": "⏰ Wake up at {}, sleep at {}, total day time: {}. 📋",
        "IDEA_EXIST": "⚠️ Idea with this name already exists. Choose another. 💡",
        "SEND_MORNING_MSG": "Good morning, {}! ☀️",
        "SEND_EVENING_MSG": "Good evening, {}! 🌙",
        "WELCOME_TO_FOCUS": "Welcome to the focus zone! 🎯",
        "START_FOCUS_MSG": "Focus session started. 🕒",
        "STOP_FOCUS_MSG": "Focus session stopped.\nDuration - {}m {}s. ⏳",
        "SAVE_FOCUS_ZONE": "Save the focus session? 📝",
        "SAVED_FOCUS_MSG": "Focus session saved. ✅",
        "NOT_SAVED_FOCUS_MSG": "Focus session not saved. ❌",
        "TITLE_FOCUS_ZONE_MSG": "Would you like to name this session? 📝",
        "NOT_FOUND_FOCUS_SESSION": "❗ Focus session start not found.",
        "FOCUS_INVALID": "Invalid option for focus",
        "FOCUS_TITLE_ASK": "Please provide the title for focus session.",
        "FOCUS_EXISTS": "❗ A focus session is already active.",
        "FOCUS_LIST_TITLE": "🧠 Your Focus Sessions",
        "NO_FOCUS_SESSIONS": "😕 No focus sessions found.",
        "DELETE_FOCUS_SESSION_MSG": "Provide a number of session which you want to delete.",
        "LANGUAGE_ASK": (
            "🌐 Choose your language. \n"
            "Select an option below. 📚"
        ),
        "LANGUAGE_OK": "✅ Language updated. Ready to proceed? 🚀",
        "LANGUAGE_INVALID": "❌ Invalid language choice. Try again. 🔢",
        "FOCUS_DELETED": "✅ Focus session #{} with the title \"{}\" has been successfully deleted.",
    }
}

# Buttons
BUTTON_SETTINGS = "⚙️ Settings"
BUTTON_ADD_TASK: str = "📝 Add a Task"
BUTTON_IDEA: str = "💾 Save an Idea"
BUTTON_MYDAY: str = "📅 My Day"
BUTTON_HELP: str = "❓ Help"
BUTTON_UA_LANG: str = "🇺🇦 Українська"
BUTTON_EN_LANG: str = "🇬🇧 English"
DEL_BUTTON: str = "🗑️ Remove Idea"
DEL_IDEA_BUTTON: str = "🗑️ Delete Idea"
SAVE_BUTTON: str = "✅ Save"
MENU_BUTTON: str = "🏠 Main Menu"
UPDATE_IDEA_BUTTON: str = "🆙 Update Idea"
ALL_IDEAS: str = "🔍 View All Ideas"
BUTTON_YES: str = "👍 Yes"
BUTTON_NO: str = "🙅 No"
BUTTON_DELETE_TASK = "🗑️ Delete Task"
BUTTON_EDIT_TASK = "✏️ Edit Task"
BUTTON_TOGGLE_STATUS = "✅ Mark Complete"
BUTTON_ALL_TASKS = "📋 All Tasks"
SETTINGS_BUTTON_LANGUAGE = "🌐 Language"
SETTINGS_BUTTON_FEEDBACK = "💬 Feedback"
SETTINGS_BUTTON_ROUTINE = "⏰ Routine"
SETTINGS_BUTTON_ROUTINE_TIME = "🕒 Routine Time"
ROUTINE_SET_WAKE_BUTTON = "⏰ Set Wake-Up Time"
ROUTINE_SET_SLEEP_BUTTON = "🛌 Set Sleep Time"
ROUTINE_MY_TIME = "⏳ My Routine"
ROUTINE_MORNING_VIEW = "🌞 Morning Routine"
ROUTINE_EVENING_VIEW = "🌙 Evening Routine"

MORNING_ROUTINE_ADD_BTN = "➕ Add Morning Routine"
MORNING_ROUTINE_DELETE_BTN = "🗑️ Delete Morning Routine"
MORNING_ROUTINE_EDIT_BTN = "✏️ Edit Morning Routine"
MY_MORNING_ROUTINE_BTN = "🌅 My Morning Routine"

EVENING_ROUTINE_ADD_BTN = "➕ Add Evening Routine"
EVENING_ROUTINE_DELETE_BTN = "🗑️ Delete Evening Routine"
EVENING_ROUTINE_EDIT_BTN = "✏️ Edit Evening Routine"
MY_EVENING_ROUTINE_BTN = "🌙 My Evening Routine"

FOCUS_ZONE_START = "🟢 Start"
FOCUS_ZONE_END = "🔴 Stop"
FOCUS_INLINE_YES = "Yes"
FOCUS_INLINE_NO = "No"
ALL_FOCUSES_BTN = "All Focuses"
DELETE_FOCUS = "Delete"

USER_FEEDBACK_MAIL_TEXT = """
📬 New feedback received!

User's input:

------------------------
{feedback}
------------------------

🧑‍💻 User Details:
- Username: {username}
- User ID: {user_id}
- Date: {date}

Please review to improve our service!
"""

def generate_daily_stats_message(language: str, created_ideas: int, completed_tasks: int, created_tasks: int) -> str:
    lang = language.upper()
    if lang == "UKRANIAN":
        return (
            "📊 Щоденна статистика:\n\n"
            f"🧠 Створено ідей: {created_ideas}\n"
            f"✅ Виконано завдань: {completed_tasks}\n"
            f"📝 Додано завдань: {created_tasks}\n\n"
            "🔄 Оновлення щодня о 00:00.\n\n"
            "Продовжуйте в тому ж дусі! 📝"
        )
    else:
        return (
            "📊 Daily Stats:\n\n"
            f"🧠 Ideas created: {created_ideas}\n"
            f"✅ Tasks completed: {completed_tasks}\n"
            f"📝 Tasks added: {created_tasks}\n\n"
            "🔄 Updates daily at 00:00.\n\n"
            "Keep up the good work! 📝"
        )

async def send_morning_message(bot: Bot, user_id: int):
    language = await UserService.get_user_language(user_id) or "ENGLISH"
    morning_routine = await RoutineService.get_user_routines(user_id, routine_type="morning")

    print(f"[INFO] - Sending morning routine to user with id, {user_id}")
    if not morning_routine:
        await bot.send_message(
            user_id,
            MESSAGES[language]['SEND_MORNING_MSG'].format("👤") + '\n' + MESSAGES[language]['NO_MORNING_ROUTINE']
        )
        return

    dividers: str = "\n" + ("-" * int(len(MESSAGES[language]['MORNING_ROUTINE_SHOW']) * 1.65))
    formatted_routine_items = "\n".join(
        f"# {idx}. {routine['routine_name']}"
        for idx, routine in enumerate(morning_routine, start=1)
    )
    formatted_morning_routine = (
        MESSAGES[language]['MORNING_ROUTINE_SHOW'] +
        dividers +
        "\n" +
        formatted_routine_items
    )

    await bot.send_message(user_id, formatted_morning_routine)

async def send_evening_message(bot: Bot, user_id: int):
    language = await UserService.get_user_language(user_id) or "ENGLISH"
    print(f"[INFO] - Sending evening routine to user with id, {user_id}")
    await bot.send_message(
        user_id,
        MESSAGES[language]['SEND_EVENING_MSG'].format("👤")
    )