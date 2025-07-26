from typing import Any

MESSAGES: Any = {
    "UKRANIAN": {
        "START_MSG": (
            "🎉 Ласкаво просимо! 🚀✨\n"
            "Готовий розпочати день продуктивно і з настроєм? 💪🔥🌟"
        ),
        "START_MSG_AGAIN": (
            "👋 Привіт знову! 🌟😊\n"
            "Рокки тут, щоб підтримати тебе і разом рухатися вперед! 🦝🔥💥\n"
            "Твій день — твої правила ✅💯"
        ),
        "HELP_MSG": (
            "ℹ️ Потрібна допомога? 🤔❓\n"
            "Напиши /start, /language або /menu — усе під рукою! 📋👇"
        ),
        "MENU_MSG": (
            "📋 **Меню, створене для тебе:** 🛠️\n"
            "Оберігай свій час ⏳, а ми подбаємо про решту 👇💡"
        ),
        "AUTHORIZATION_PROBLEM": (
            "🚫 Упс! Здається, ти не авторизований 🙈🔒\n"
            "Напиши /start, щоб почати ✅🚀"
        ),
        "TEXT_RESPONSE": (
            "✉️ Ти написав: \"{response}\" 📝.\n"
            "Дякуємо за відповідь! 🙌🌟"
        ),
        "CONTINUE_MSG": (
            "✨ Що б ти хотів зробити далі? 🤔✅\n"
            "Відкрий /menu і обирай — я поруч і готовий допомогти! 🦝💪"
        ),
        "SETTINGS_RESPONSE": "🔧 Відкриваю налаштування... ⚙️🔄",
        "MYDAY_RESPONSE": "📅 Ось твій план на сьогодні! ✅🔥",
        "IDEA_RESPONSE": "💡 Маєш ідею? Напиши її тут — я збережу! 📝✅",
        "IDEA_SAVED": "✅ Ідея успішно збережена! 🎯✨",
        "ADD_TASK_RESPONSE": "📝 Додаємо нове завдання... ⏳✅",
        "IDEA_ACTION": "📌 Що хочеш зробити з цією ідеєю? 🤔🔄",
        "IDEA_DELETE": "🗑️ Ідею видалено! ✅💥",
        "IDEA_PROBLEM": "⚠️ Виникла проблема із збереженням ідеї. 😕🔄 Спробуй ще раз!",
        "IDEAS_SHOW": "💡 Ось твої ідеї: 📋✨",
        "IDEA_EXISTS": "⚠️ Така ідея вже існує! 🔄🔍",
        "ERROR_SAVING_IDEA": "⚠️ Помилка при збереженні. ⏳ Спробуй пізніше.",
        "NO_IDEAS": "📝 У тебе ще немає ідей. Додай першу! 🚀✅",
        "DELETE_IDEA": "ℹ️ Вкажи номер ідеї для видалення 🔢🗑️",
        "UPDATE_IDEA": "ℹ️ Вкажи номер ідеї для оновлення 🔢✏️",
        "NOT_VALID_IDEA_NUM": "❌ Введи дійсний номер. 🔄🧐",
        "INVALID_IDEA_NUM": "❌ Неправильний номер. Спробуй ще раз! 🔄🔍",
        "IDEA_DELETED": "🗑️ Ідею №{} '{}' видалено! ✅💥",
        "ASK_NEW_IDEA_TEXT": "✏️ Введи новий текст для ідеї №{} '{}': 📝",
        "IDEA_UPDATED": "✅ Ідею №{} успішно оновлено! 🎯🔥",
        "TASK_ADD": "📝 Введи назву завдання та натисни кнопку ⬇️👇",
        "TASK_DEADLINE_ASK": "⏰ Додати дедлайн для завдання? ⏳",
        "TASK_DEADLINE_YES": "🕒 Введи час (дедлайн), наприклад: 13:10 🗓️",
        "TASK_DEADLINE_NO": "✅ Завдання без дедлайну збережено! 🏆",
        "TASK_DEADLINE_INVALID": "❌ Невірний час! Спробуй ще раз. 🔄⏳",
        "TASK_SAVED": "✅ Завдання збережено! 🏆🎉",
        "TASK_MENU": "📂 Меню завдань 📝🔧",
        "NO_TASKS": "❌ Завдань ще немає! Додай перше через /task ✅🚀",
        "YOUR_TASKS": "📋 Твої завдання: ✅📌",
        "TASK_DELETE_MSG": "🗑️ Вкажи номер завдання для видалення 🔢❗",
        "INVALID_TASK_NUM": "❌ Невірний номер! 🔄⚠️",
        "TASK_DELETED": "✅ Завдання №{} '{}' видалено! 🗑️💥",
        "TASK_DELETE_PROBLEM": "⚠️ Помилка при видаленні. Спробуй пізніше! ⏳",
        "COMPLETE_TASK_MSG": "✅ Вкажи номер виконаного завдання 🏆🎯",
        "COMPLETE_TASK_INVALID": "❌ Неправильний номер! 🔄⚠️",
        "COMPLETE_TASK_SUCCESS": "🏆 Завдання №{} '{}' виконано! Молодець! 🎉✅",
        "COMPLETE_TASK_PROBLEM": "⚠️ Помилка оновлення! 🔄😕",
        "UPDATE_TASK_MSG": "✏️ Вкажи номер завдання для оновлення 🔢📝",
        "UPDATE_TASK_INVALID": "❌ Невірний номер! 🔄⚠️",
        "UPDATE_TASK_SUCCESS": "✅ Завдання №{} оновлено! 🏆🔥",
        "UPDATE_TASK_PROBLEM": "⚠️ Проблема при оновленні. 😕🔄",
        "UPDATE_TASK_NAME_MSG": "📝 Введи нову назву завдання: ✏️",
        "UPDATE_TASK_NAME_INVALID": "❌ Неправильна назва! 🔄⚠️",
        "SETTINGS_MENU": "⚙️ Ласкаво просимо в налаштування 🛠️🔧",
        "ROUTINE_MENU_DAY": "Встанови розпорядок — Morning / Evening 🌅🌙✨",
        "MORNING_ROUTINE": "Твій ранковий розпорядок ☀️🌞💪",
        "EVENING_ROUTINE": "Твій вечірній розпорядок 🌙⭐🛌",
        "ROUTINES_INVALID": "Упс, щось пішло не так ❌😕",
        "ADD_MORNING_ROUTINE": "Введи назву розпорядку 📝✨",
        "INVALID_MORNING_ROUTINE": "❌ Введи дійсний заголовок. 🔄⚠️",
        "ROUTINE_EXISTS": "Такий розпорядок вже існує. 🔄🗂️",
        "ROUTINE_SAVED": "Розпорядок «{}» успішно збережено! ✅🎉",
        "MORNING_ROUTINE_SHOW": "Твої ранкові розпорядки ☀️🗒️",
        "EVENING_ROUTINE_SHOW": "Твої вечірні розпорядки 🌙📝",
        "NO_MORNING_ROUTINE": "Ранковий розпорядок ще не встановлено. Встанови його, щоб тримати режим у порядку! 🚀✅",
        "PROVIDE_ROUTINE_ID": "Вкажи номер розпорядку 🔢👇",
        "ROUTINE_DELETED": "Розпорядок видалено 🗑️✅",
        "NEW_ROUTINE_NAME": "Введи нову назву розпорядку: ✏️",
        "ROUTINE_NAME_SET": "Нову назву розпорядку змінено на «{}». ✅✨",
        "SMTP_MESSAGE_TEXT": "Залиши свій відгук нижче: 📝💬",
        "SMTP_MESSAGE_SENT": "Дякуємо за відгук! Наша команда це цінує! 🙏💖",
        "INVALID_MESSAGE": "Введи коректний текст. ❌🔄",
        "LANGUAGE_ASK": (
            "🌐 **Оберіть мову:** 🌍🗣️\n"
            "Натисни кнопку нижче ⬇️👇"
        ),
        "LANGUAGE_OK": "✅ Мову успішно оновлено! 🚀🎉",
        "LANGUAGE_INVALID": "⚠️ Недійсний вибір. Спробуй ще раз! 🔄❗"
    },

    "ENGLISH": {
        "START_MSG": (
            "🎉 Welcome! 🚀✨\n"
            "Ready to start your productive day with good vibes? 💪🔥🌟"
        ),
        "START_MSG_AGAIN": (
            "👋 Welcome back! 🌟😊\n"
            "Rocky’s here to support you and keep you going! 🦝🔥💥\n"
            "Your day, your rules ✅💯"
        ),
        "HELP_MSG": (
            "ℹ️ Need help? 🤔❓\n"
            "Use /start, /language or /menu — everything is here! 📋👇"
        ),
        "MENU_MSG": (
            "📋 **Your personalized menu:** 🛠️\n"
            "Protect your time ⏳, and we’ll handle the rest 👇💡"
        ),
        "AUTHORIZATION_PROBLEM": (
            "🚫 Oops! You’re not authorized 🙈🔒\n"
            "Type /start to get going ✅🚀"
        ),
        "TEXT_RESPONSE": (
            "✉️ You wrote: \"{response}\" 📝.\n"
            "Thanks for your input! 🙌🌟"
        ),
        "CONTINUE_MSG": (
            "✨ What do you want to do next? 🤔✅\n"
            "Open /menu and choose — I’m here to help! 🦝💪"
        ),
        "SETTINGS_RESPONSE": "🔧 Opening settings... ⚙️🔄",
        "MYDAY_RESPONSE": "📅 Here’s your plan for today! ✅🔥",
        "IDEA_RESPONSE": "💡 Got an idea? Type it — I’ll save it! 📝✅",
        "IDEA_SAVED": "✅ Idea saved successfully! 🎯✨",
        "ADD_TASK_RESPONSE": "📝 Adding a new task... ⏳✅",
        "IDEA_ACTION": "📌 What do you want to do with this idea? 🤔🔄",
        "IDEA_DELETE": "🗑️ Idea deleted! ✅💥",
        "IDEA_PROBLEM": "⚠️ Problem saving your idea. 😕🔄 Try again!",
        "IDEAS_SHOW": "💡 Here are your ideas: 📋✨",
        "IDEA_EXISTS": "⚠️ That idea already exists! 🔄🔍",
        "ERROR_SAVING_IDEA": "⚠️ Error saving. ⏳ Try later.",
        "NO_IDEAS": "📝 No ideas yet. Add your first! 🚀✅",
        "DELETE_IDEA": "ℹ️ Enter idea number to delete 🔢🗑️",
        "UPDATE_IDEA": "ℹ️ Enter idea number to update 🔢✏️",
        "NOT_VALID_IDEA_NUM": "❌ Enter a valid number. 🔄🧐",
        "INVALID_IDEA_NUM": "❌ Invalid number. Try again! 🔄🔍",
        "IDEA_DELETED": "🗑️ Idea #{} '{}' deleted! ✅💥",
        "ASK_NEW_IDEA_TEXT": "✏️ Enter new text for idea #{} '{}': 📝",
        "IDEA_UPDATED": "✅ Idea #{} updated! 🎯🔥",
        "TASK_ADD": "📝 Enter task name and press the button ⬇️👇",
        "TASK_DEADLINE_ASK": "⏰ Add a deadline for the task? ⏳",
        "TASK_DEADLINE_YES": "🕒 Enter time (deadline), e.g. 13:10 🗓️",
        "TASK_DEADLINE_NO": "✅ Task saved without deadline! 🏆",
        "TASK_DEADLINE_INVALID": "❌ Invalid time! Try again. 🔄⏳",
        "TASK_SAVED": "✅ Task saved! 🏆🎉",
        "TASK_MENU": "📂 Task menu 📝🔧",
        "NO_TASKS": "❌ No tasks yet! Add your first with /task ✅🚀",
        "YOUR_TASKS": "📋 Your tasks: ✅📌",
        "TASK_DELETE_MSG": "🗑️ Enter task number to delete 🔢❗",
        "INVALID_TASK_NUM": "❌ Invalid number! 🔄⚠️",
        "TASK_DELETED": "✅ Task #{} '{}' deleted! 🗑️💥",
        "TASK_DELETE_PROBLEM": "⚠️ Problem deleting. Try later! ⏳",
        "COMPLETE_TASK_MSG": "✅ Enter completed task number 🏆🎯",
        "COMPLETE_TASK_INVALID": "❌ Invalid number! 🔄⚠️",
        "COMPLETE_TASK_SUCCESS": "🏆 Task #{} '{}' marked complete! Well done! 🎉✅",
        "COMPLETE_TASK_PROBLEM": "⚠️ Error updating! 🔄😕",
        "UPDATE_TASK_MSG": "✏️ Enter task number to update 🔢📝",
        "UPDATE_TASK_INVALID": "❌ Invalid number! 🔄⚠️",
        "UPDATE_TASK_SUCCESS": "✅ Task #{} updated! 🏆🔥",
        "UPDATE_TASK_PROBLEM": "⚠️ Problem updating. 😕🔄",
        "UPDATE_TASK_NAME_MSG": "📝 Enter new task name: ✏️",
        "UPDATE_TASK_NAME_INVALID": "❌ Invalid name! 🔄⚠️",
        "SETTINGS_MENU": "⚙️ Welcome to Settings 🛠️🔧",
        "ROUTINE_MENU_DAY": "Set your routine — Morning / Evening 🌅🌙✨",
        "MORNING_ROUTINE": "Your morning routine ☀️🌞💪",
        "EVENING_ROUTINE": "Your evening routine 🌙⭐🛌",
        "ROUTINES_INVALID": "Oops, something went wrong ❌😕",
        "ADD_MORNING_ROUTINE": "Enter routine title 📝✨",
        "INVALID_MORNING_ROUTINE": "❌ Enter valid title. 🔄⚠️",
        "ROUTINE_EXISTS": "Routine with this title already exists. 🔄🗂️",
        "ROUTINE_SAVED": "Routine «{}» saved successfully! ✅🎉",
        "MORNING_ROUTINE_SHOW": "Your morning routines ☀️🗒️",
        "EVENING_ROUTINE_SHOW": "Your evening routines 🌙📝",
        "NO_MORNING_ROUTINE": "No morning routine yet. Set one to keep your schedule! 🚀✅",
        "PROVIDE_ROUTINE_ID": "Enter routine number 🔢👇",
        "ROUTINE_DELETED": "Routine deleted 🗑️✅",
        "NEW_ROUTINE_NAME": "Enter new routine name: ✏️",
        "ROUTINE_NAME_SET": "Routine name changed to «{}». ✅✨",
        "SMTP_MESSAGE_TEXT": "Leave your feedback below: 📝💬",
        "SMTP_MESSAGE_SENT": "Thanks for your feedback! The team appreciates it! 🙏💖",
        "INVALID_MESSAGE": "Please enter valid text. ❌🔄",
        "LANGUAGE_ASK": (
            "🌐 **Choose your language:** 🌍🗣️\n"
            "Tap a button below ⬇️👇"
        ),
        "LANGUAGE_OK": "✅ Language updated! 🚀🎉",
        "LANGUAGE_INVALID": "⚠️ Invalid choice. Try again! 🔄❗"
    }
}


# Buttons
BUTTON_ADD_TASK: str = "📝 Create Task"
BUTTON_IDEA: str = "💾 Save Idea"
BUTTON_MYDAY: str = "📅 My Day"
BUTTON_SETTINGS: str = "⚙️ Settings"
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
BUTTON_EDIT_TASK = "✏️️ Edit Task"
BUTTON_TOGGLE_STATUS = "✅ Complete"
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

MORNINGG_ROUTINE_ADD_BTN  = "➕ Add Morning"
MORNING_ROUTINE_DELETE_BTN = "🗑️ Delete Morning"
MORNING_ROUTINE_EDIT_BTN = "✏️ Edit Morning"
MY_MORNING_ROUTINE_BTN = "🌅 My Morning Routine"

EVENING_ROUTINE_ADD_BTN = "➕ Add Evening"
EVENING_ROUTINE_DELETE_BTN = "🗑️ Delete Evening"
EVENING_ROUTINE_EDIT_BTN = "✏️ Edit Evening"
MY_EVENING_ROUTINE_BTN = "🌙 My Evening Routine"


USER_FEEDBACK_MAIL_TEXT = """
📬 New User Feedback Received!

Here’s what the user had to say:

------------------------
{feedback}
------------------------

🧑‍💻 User Info:
- Username: {username}
- User ID: {user_id}
- Date: {date}

Please review it and take action if needed.
"""

def generate_daily_stats_message(language: str, created_ideas: int, completed_tasks: int, created_tasks: int) -> str:
    lang = language.upper()
    if lang == "UKRANIAN":
        return (
            "📊 *Твоя щоденна статистика:*\n\n"
            f"🧠 *Створено ідей*: `{created_ideas}`\n"
            f"✅ *Виконано завдань*: `{completed_tasks}`\n"
            f"📝 *Додано завдань*: `{created_tasks}`\n\n"
            "🔁 Автоматичне оновлення щодня о *00:00*.\n\n"
            "Так тримати! Ти молодець 💪🔥"
        )
    else:
        return (
            "📊 *Your Daily Stats:*\n\n"
            f"🧠 *Ideas created*: `{created_ideas}`\n"
            f"✅ *Tasks completed*: `{completed_tasks}`\n"
            f"📝 *Tasks added*: `{created_tasks}`\n\n"
            "🔁 Auto-updated every day at *00:00*.\n\n"
            "Keep it up! You’re crushing it 💪🚀"
        )