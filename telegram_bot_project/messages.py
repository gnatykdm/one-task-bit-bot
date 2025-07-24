from typing import Any

MESSAGES: Any = {
    "UKRANIAN": {
        "START_MSG": "🎉 Ласкаво просимо! 🚀 Готові розпочати свій продуктивний день? 💪",
        "START_MSG_AGAIN": "👋 Радий знову бачити вас! 🌟 Продовжимо досягати цілей разом ✅",
        "HELP_MSG": "ℹ️ Потрібна допомога? 🤔\nВикористовуйте /start, /language або /menu – усе під рукою! 📋",
        "MENU_MSG": "📋 **Меню доступних дій:**\nВиберіть, що хочете зробити 👇",
        "AUTHORIZATION_PROBLEM": "🚫 Здається, ви не авторизовані! 🙈\nВведіть /start, щоб почати ✅",
        "TEXT_RESPONSE": "✉️ Ви написали: \"{response}\".\nДякуємо за відповідь! 🙌",
        "CONTINUE_MSG": "✨ Що ще зробимо? ✅\nВідкрийте /menu для всіх можливостей 🌟",
        "SETTINGS_RESPONSE": "🔧 Відкриваю налаштування... ⚙️",
        "MYDAY_RESPONSE": "📅 Ось ваш план на сьогодні! ✅",
        "IDEA_RESPONSE": "💡 Маєте ідею? Напишіть її тут — я збережу! ✅",
        "IDEA_SAVED": "✅ Ідея успішно збережена! 🎯",
        "ADD_TASK_RESPONSE": "📝 Додаємо нове завдання... ✅",
        "IDEA_ACTION": "📌 Що бажаєте зробити з цією ідеєю?",
        "IDEA_DELETE": "🗑️ Ідею видалено! ✅",
        "IDEA_PROBLEM": "⚠️ Виникла проблема із збереженням ідеї. 😕 Спробуйте ще раз!",
        "IDEAS_SHOW": "💡 Ось ваші ідеї: ",
        "IDEA_EXISTS": "⚠️ Ця ідея вже існує! 🔄",
        "ERROR_SAVING_IDEA": "⚠️ Помилка при збереженні. 😕 Спробуйте ще раз.",
        "NO_IDEAS": "📝 У вас ще немає ідей. ✅ Додайте першу!",
        "DELETE_IDEA": "ℹ️ Вкажіть номер ідеї, яку хочете видалити 🔢",
        "UPDATE_IDEA": "ℹ️ Вкажіть номер ідеї для оновлення 🔢",
        "NOT_VALID_IDEA_NUM": "❌ Введіть дійсний номер. 🔄",
        "INVALID_IDEA_NUM": "❌ Неправильний номер. Спробуйте ще раз! 🔄",
        "IDEA_DELETED": "🗑️ Ідею №{} '{}' видалено! ✅",
        "ASK_NEW_IDEA_TEXT": "✏️ Введіть новий текст для ідеї №{} '{}':",
        "IDEA_UPDATED": "✅ Ідею №{} успішно оновлено! 🎯",
        "TASK_ADD": "📝 Введіть назву завдання та натисніть кнопку нижче ⬇️",
        "TASK_DEADLINE_ASK": "⏰ Додати крайній термін для цього завдання?",
        "TASK_DEADLINE_YES": "🕒 Введіть час (дедлайн):\nНаприклад: 13:10",
        "TASK_DEADLINE_NO": "✅ Завдання без дедлайну збережено!",
        "TASK_DEADLINE_INVALID": "❌ Недійсний час! ⏰ Спробуйте ще раз.",
        "TASK_SAVED": "✅ Завдання збережено! 🏆",
        "TASK_MENU": "📂 Меню завдань 📝",
        "NO_TASKS": "❌ Немає завдань! Додайте перше через /task ✅",
        "YOUR_TASKS": "📋 Ваші завдання:",
        "TASK_DELETE_MSG": "🗑️ Введіть номер завдання для видалення 🔢",
        "INVALID_TASK_NUM": "❌ Невірний номер завдання! 🔄",
        "TASK_DELETED": "✅ Завдання №{} '{}' видалено! 🗑️",
        "TASK_DELETE_PROBLEM": "⚠️ Помилка при видаленні. 😕 Спробуйте пізніше!",
        "COMPLETE_TASK_MSG": "✅ Введіть номер завдання, яке виконано 🏆",
        "COMPLETE_TASK_INVALID": "❌ Неправильний номер! 🔄",
        "COMPLETE_TASK_SUCCESS": "🏆 Завдання №{} '{}' виконано! ✅",
        "COMPLETE_TASK_PROBLEM": "⚠️ Помилка під час оновлення! 🔄",
        "UPDATE_TASK_MSG": "✏️ Введіть номер завдання для оновлення 🔢",
        "UPDATE_TASK_INVALID": "❌ Невірний номер! 🔄",
        "UPDATE_TASK_SUCCESS": "✅ Завдання №{} оновлено! 🏆",
        "UPDATE_TASK_PROBLEM": "⚠️ Помилка під час оновлення. 😕",
        "UPDATE_TASK_NAME_MSG": "📝 Введіть нову назву завдання:",
        "UPDATE_TASK_NAME_INVALID": "❌ Неправильна назва! 🔄",
        "SETTINGS_MENU": "⚙️ Ласкаво просимо в Налаштування",
        "ROUTINE_MENU_DAY": "Встановіть розпорядок за кнопками -> Morning / Evening",
        "ROUTINE_TIME": (
            "⏰ Ваш розпорядок:\n"
            "• Час підйому: {}\n"
            "• Час сну: {}\n"
            "• Загальна кількість годин: {}"
        ),
        "ROUTINE_TIME_NOT": "⚠️ Ви ще не встановили час підйому та сну. Налаштуйте їх, щоб тримати розпорядок під контролем!",
        "ROUTINE_MENU": "🛠 Ласкаво просимо до налаштувань розпорядку! Тут ви можете встановити час підйому та сну.",
        "SET_WAKE_TIME_MSG": "🌅 Введіть час підйому у 24-годинному форматі (ГГ:ХХ):",
        "WAKE_TIME_SET": "✅ Час підйому успішно встановлено на {}.",
        "SET_SLEEP_TIME_MSG": "🌙 Введіть час сну у 24-годинному форматі (ГГ:ХХ):",
        "SLEEP_TIME_SET": "✅ Час сну успішно встановлено на {}.",
        "LANGUAGE_ASK": (
            "🌐 **Оберіть мову інтерфейсу:**\n"
            "Натисніть кнопку нижче ⬇️"
        ),
        "LANGUAGE_OK": (
            "✅ Мову успішно оновлено! 🚀"
        ),
        "LANGUAGE_INVALID": (
            "⚠️ Недійсний вибір. Спробуйте ще раз! 🔄"
        )
    },

    "ENGLISH": {
        "START_MSG": "🎉 Welcome! 🚀 Ready to start your productive day? 💪",
        "START_MSG_AGAIN": "👋 Welcome back! 🌟 Let’s keep reaching goals together ✅",
        "HELP_MSG": "ℹ️ Need help? 🤔\nUse /start, /language or /menu – everything is here! 📋",
        "MENU_MSG": "📋 **Here’s your menu:**\nChoose an option below 👇",
        "AUTHORIZATION_PROBLEM": "🚫 Looks like you’re not authorized! 🙈\nType /start to begin ✅",
        "TEXT_RESPONSE": "✉️ You wrote: \"{response}\".\nThanks for sharing! 🙌",
        "CONTINUE_MSG": "✨ What else can I do for you? ✅\nOpen /menu for all options 🌟",
        "SETTINGS_RESPONSE": "🔧 Opening your settings... ⚙️",
        "MYDAY_RESPONSE": "📅 Here’s your plan for today! ✅",
        "IDEA_RESPONSE": "💡 Got an idea? Type it here – I’ll save it! ✅",
        "IDEA_SAVED": "✅ Idea saved successfully! 🎯",
        "ADD_TASK_RESPONSE": "📝 Creating a new task... ✅",
        "IDEA_ACTION": "📌 What would you like to do with this idea?",
        "IDEA_DELETE": "🗑️ Idea deleted! ✅",
        "IDEA_PROBLEM": "⚠️ There was an issue saving your idea. 😕 Please try again!",
        "IDEAS_SHOW": "💡 Here are your ideas: ",
        "IDEA_EXISTS": "⚠️ This idea already exists! 🔄",
        "ERROR_SAVING_IDEA": "⚠️ Error saving the idea. 😕 Try again later.",
        "NO_IDEAS": "📝 You don’t have any ideas yet. ✅ Add one now!",
        "DELETE_IDEA": "ℹ️ Enter the idea number you want to delete 🔢",
        "UPDATE_IDEA": "ℹ️ Enter the idea number you want to update 🔢",
        "NOT_VALID_IDEA_NUM": "❌ Please enter a valid number. 🔄",
        "INVALID_IDEA_NUM": "❌ Invalid number. Please try again! 🔄",
        "IDEA_DELETED": "🗑️ Idea #{} '{}' deleted! ✅",
        "ASK_NEW_IDEA_TEXT": "✏️ Please enter the new text for idea #{} '{}':",
        "IDEA_UPDATED": "✅ Idea #{} updated successfully! 🎯",
        "TASK_ADD": "📝 Enter the task name and press the button below ⬇️",
        "TASK_DEADLINE_ASK": "⏰ Add a deadline for this task?",
        "TASK_DEADLINE_YES": "🕒 Enter the time (deadline):\nExample: 13:10",
        "TASK_DEADLINE_NO": "✅ Task saved without a deadline!",
        "TASK_DEADLINE_INVALID": "❌ Invalid time! ⏰ Please try again.",
        "TASK_SAVED": "✅ Task saved successfully! 🏆",
        "TASK_MENU": "📂 Task menu 📝",
        "NO_TASKS": "❌ No tasks yet! Add your first one using /task ✅",
        "YOUR_TASKS": "📋 Your tasks:",
        "TASK_DELETE_MSG": "🗑️ Enter the task number to delete 🔢",
        "INVALID_TASK_NUM": "❌ Invalid task number! 🔄",
        "TASK_DELETED": "✅ Task #{} '{}' deleted! 🗑️",
        "TASK_DELETE_PROBLEM": "⚠️ Problem deleting task. 😕 Try again later!",
        "COMPLETE_TASK_MSG": "✅ Enter the number of the completed task 🏆",
        "COMPLETE_TASK_INVALID": "❌ Invalid number! 🔄",
        "COMPLETE_TASK_SUCCESS": "🏆 Task #{} '{}' marked as complete! ✅",
        "COMPLETE_TASK_PROBLEM": "⚠️ Error updating status! 🔄",
        "UPDATE_TASK_MSG": "✏️ Enter the task number to update 🔢",
        "UPDATE_TASK_INVALID": "❌ Invalid number! 🔄",
        "UPDATE_TASK_SUCCESS": "✅ Task #{} updated successfully! 🏆",
        "UPDATE_TASK_PROBLEM": "⚠️ Problem updating task. 😕",
        "UPDATE_TASK_NAME_MSG": "📝 Enter the new task name:",
        "UPDATE_TASK_NAME_INVALID": "❌ Invalid task name! 🔄",
        "SETTINGS_MENU": "⚙️ Welcome to Settings",
        "ROUTINE_MENU_DAY": "Set the routine from buttons -> Morning/Evening",
        "ROUTINE_TIME": (
            "⏰ Your routine:\n"
            "• Wake-up time: {}\n"
            "• Sleep time: {}\n"
            "• Total hours awake: {}"
        ),
        "ROUTINE_TIME_NOT": "⚠️ You haven’t set your wake-up and sleep times yet. Set them to keep your routine on track!",
        "ROUTINE_MENU": "🛠 Welcome to your Routine Settings! Customize your wake-up and sleep times here.",
        "SET_WAKE_TIME_MSG": "🌅 Please enter your wake-up time in 24-hour format (HH:MM):",
        "WAKE_TIME_SET": "✅ Wake-up time successfully set to {}.",
        "SET_SLEEP_TIME_MSG": "🌙 Please enter your sleep time in 24-hour format (HH:MM):",
        "SLEEP_TIME_SET": "✅ Sleep time successfully set to {}.",
        "LANGUAGE_ASK": (
            "🌐 **Choose your language:**\n"
            "Tap a button below ⬇️"
        ),
        "LANGUAGE_OK": (
            "✅ Language updated successfully! 🚀"
        ),
        "LANGUAGE_INVALID": (
            "⚠️ Invalid choice. Please try again! 🔄"
        )
    }
}

# Buttons
BUTTON_ADD_TASK: str = "📝 Create Task"
BUTTON_IDEA: str = "💡 Save Idea"
BUTTON_MYDAY: str = "📅 My Day"
BUTTON_SETTINGS: str = "⚙️ Settings"
BUTTON_HELP: str = "❓ Help"
BUTTON_UA_LANG: str = "🌻 Українська"
BUTTON_EN_LANG: str = "🇬🇧 English"
DEL_BUTTON: str = "🗑️ Remove Idea"
DEL_IDEA_BUTTON: str = "🗑️ Delete Idea"
SAVE_BUTTON: str = "✅ Save"
MENU_BUTTON: str = "📂 Main Menu"
UPDATE_IDEA_BUTTON: str = "✏️ Update Idea"
ALL_IDEAS: str = "📋 View All Ideas"
BUTTON_YES: str = "✅ Yes"
BUTTON_NO: str = "❌ No"
BUTTON_DELETE_TASK = "🗑️ Delete Task"
BUTTON_EDIT_TASK = "✏️ Edit Task"
BUTTON_TOGGLE_STATUS = "✅ Complete"
BUTTON_ALL_TASKS = "📂 All tasks"
SETTINGS_BUTTON_LANGUAGE = "🌐 Language"
SETTINGS_BUTTON_FEEDBACK = "💬 Feedback"
SETTINGS_BUTTON_ROUTINE = "✅ Routine"
SETTINGS_BUTTON_ROUTINE_TIME = "⏰ Routine Time"
ROUTINE_SET_WAKE_BUTTON = "🌅 Set Wake-Up Time"
ROUTINE_SET_SLEEP_BUTTON = "🌙 Set Sleep Time"
ROUTINE_MY_TIME = "🕒 My Routine"
ROUTINE_MORNING_VIEW = "Morning Routine"
ROUTINE_EVENING_VIEW = "Afternoon Routine"