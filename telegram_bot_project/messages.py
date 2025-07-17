from typing import Any

MESSAGES: Any = {
    "UKRANIAN": {
        "START_MSG": "🎉 Ласкаво просимо до бота!\nГотові розпочати свій продуктивний день разом зі мною?",
        "START_MSG_AGAIN": "👋 Вітаю з поверненням, чемпіоне!\nРадий знову бачити вас 😊",
        "HELP_MSG": "ℹ️ Потрібна допомога?\nСпробуйте /start, /language або /menu — я завжди поруч, щоб допомогти 📋",
        "MENU_MSG": "📋 **Ось ваше меню:**\nОберіть потрібну дію 👇",
        "AUTHORIZATION_PROBLEM": "🚫 Упс, здається, ви не авторизовані.\nБудь ласка, введіть /start, щоб почати.",
        "TEXT_RESPONSE": "✉️ Ви написали: \"{response}\".\nДякую, що поділилися! 🙌",
        "CONTINUE_MSG": "✨ Чим ще можу допомогти?\nСміливо відкривайте /menu для всіх можливостей 🌟",
        "SETTINGS_RESPONSE": "🔧 Відкриваю налаштування для вас...",
        "MYDAY_RESPONSE": "📅 Ось ваш план на сьогодні...",
        "IDEA_RESPONSE": "💡 Розкажіть свою ідею — я обов’язково її зафіксую!",
        "IDEA_SAVED": "💡 Ідея успішно збережена. Молодець!",
        "ADD_TASK_RESPONSE": "📝 Створюємо нове завдання...",
        "IDEA_ACTION": "Що бажаєте зробити з цією ідеєю?",
        "IDEA_DELETE": "🗑️ Ідею було видалено.",
        "IDEA_PROBLEM": "⚠️ Виникла проблема із збереженням ідеї. Спробуйте ще раз.",
        "IDEAS_SHOW": "💡 Усі ваші ідеї: ",
        "IDEA_EXISTS": "⚠️ Ця ідея вже існує.",
        "ERROR_SAVING_IDEA": "⚠️ Проблема із збереженням ідеї. Спробуйте ще раз.",
        "NO_IDEAS": "📝 Ви ще не маєте ідей.",
        "DELETE_IDEA": "ℹ️ Вкажіть номер ідеї, яку хочете видалити",
        "UPDATE_IDEA": "ℹ️ Вкажіть номер ідеї, яку хочете обновити",
        "NOT_VALID_IDEA_NUM": "❌ Будь ласка, введіть дійсний номер.",
        "INVALID_IDEA_NUM": "❌ Неправильний номер. Спробуйте ще раз.",
        "IDEA_DELETED": "🗑️ Ідею №{} '{}' було видалено.",
        "ASK_NEW_IDEA_TEXT": "✏️ Введіть новий текст для ідеї №{} '{}'.",
        "IDEA_UPDATED": "✅ Ідею №{} успішно оновлено.",
        "TASK_ADD": "Вкажіть назву завдання та натисніть кнопку нижче, щоб продовжити",
        "TASK_DEADLINE_ASK": "Це завдання має крайній термін?",
        "TASK_DEADLINE_YES": "Будьласка введіть годину (дедлайн) для задачі.\nПриклад: 13:10",
        "TASK_DEADLINE_NO": "Гаразд, без крайнього терміну. Ваше завдання збережено.",
        "TASK_DEADLINE_INVALID": "Недійсний термін. Будь ласка, спробуйте ще раз.",
        "TASK_SAVED": "Задачу збережено.",
        "TASK_MENU": "Меню задач",
        "NO_TASKS": "Наразі у вас немає задач. Для добалення - /task",
        "YOUR_TASKS": "Ваші задачі:",
        "TASK_DELETE_MSG": "Будьласка введіть номер задачі яку зочете видалити",
        "INVALID_TASK_NUM": "Поганий номер задачі",
        "TASK_DELETED": "Завдання №{} '{}' було видалено.",
        "TASK_DELETE_PROBLEM": "Проблема з видаленням завдання. Спробуйте пізніше.",
        "COMPLETE_TASK_MSG": "Введіть номер завдання, яке ви хочете позначити як виконане",
        "COMPLETE_TASK_INVALID": "Невірний номер завдання. Спробуйте ще раз.",
        "COMPLETE_TASK_SUCCESS": "Завдання №{} '{}' успішно позначено як виконане.",
        "COMPLETE_TASK_PROBLEM": "Проблема з позначенням завдання як виконаного. Спробуйте пізніше.",
        "LANGUAGE_ASK": (
            "🌐 **Оберіть мову інтерфейсу:**\n"
            "Натисніть кнопку нижче, щоб продовжити:"
        ),
        "LANGUAGE_OK": (
            "✅ **Мову успішно оновлено!**\n"
            "Продовжуємо працювати разом."
        ),
        "LANGUAGE_INVALID": (
            "⚠️ Упс! Цей варіант недійсний.\n"
            "Будь ласка, оберіть мову зі списку."
        )
    },
    "ENGLISH": {
        "START_MSG": "🎉 Welcome to the bot!\nReady to start a productive day together?",
        "START_MSG_AGAIN": "👋 Welcome back, legend!\nGlad to see you again 😊",
        "HELP_MSG": "ℹ️ Need help?\nTry /start, /language, or /menu — I’m here for you 📋",
        "MENU_MSG": "📋 **Here’s your menu:**\nChoose what you'd like to do 👇",
        "AUTHORIZATION_PROBLEM": "🚫 Oops! You’re not authorized yet.\nPlease type /start to begin.",
        "TEXT_RESPONSE": "✉️ You wrote: \"{response}\".\nThanks for sharing! 🙌",
        "CONTINUE_MSG": "✨ What else can I do for you?\nFeel free to use /menu for all options 🌟",
        "SETTINGS_RESPONSE": "🔧 Opening your settings now...",
        "MYDAY_RESPONSE": "📅 Here’s your plan for today...",
        "IDEA_RESPONSE": "💡 Share your idea with me — I’ll save it safely!",
        "IDEA_SAVED": "💡 Idea saved successfully. Well done!",
        "ADD_TASK_RESPONSE": "📝 Creating a new task...",
        "IDEA_ACTION": "What would you like to do with your idea?",
        "IDEA_DELETE": "🗑️ Idea has been deleted.",
        "IDEA_PROBLEM": "⚠️ There was an issue saving your idea. Please try again.",
        "IDEAS_SHOW": "💡 Here are your ideas: ",
        "IDEA_EXISTS": "⚠️ This idea already exists",
        "ERROR_SAVING_IDEA": "⚠️ Error saving the idea. Please try again later.",
        "DELETE_IDEA": "ℹ️ Enter the idea number you want to delete",
        "UPDATE_IDEA": "ℹ️ Enter the idea number you want to update",
        "NOT_VALID_IDEA_NUM": "❌ Please enter a valid number.",
        "INVALID_IDEA_NUM": "❌ Invalid number. Please try again.",
        "NO_IDEAS": "📝 You don't have any ideas yet. Be the first to save one!",
        "IDEA_DELETED": "🗑️ Idea #{} '{}' has been deleted.",
        "ASK_NEW_IDEA_TEXT": "✏️ Please enter the new text for idea #{} '{}'.",
        "IDEA_UPDATED": "✅ Idea №{} updated successfully.",
        "TASK_ADD": "Provide a task name and press the button below to continue",
        "TASK_DEADLINE_ASK": "This task have a deadline?",
        "TASK_DEADLINE_YES": "Please enter the time (deadline) for the task.\nExample: 13:10",
        "TASK_DEADLINE_NO": "Ok, no deadline. Your task saved.",
        "TASK_DEADLINE_INVALID": "Invalid deadline. Please try again.",
        "TASK_SAVED": "Task saved successfully.",
        "TASK_MENU": "Task menu",
        "NO_TASKS": "You are actually dont have any tasks yet. Be the first to add one! /task",
        "YOUR_TASKS": "Your tasks:",
        "TASK_DELETE_MSG": "Please enter the task number you want to delete",
        "INVALID_TASK_NUM": "Invalid task number",
        "TASK_DELETED": "Task #{} '{}' has been deleted.",
        "TASK_DELETE_PROBLEM": "Problem with deleting task. Please try again later.",
        "COMPLETE_TASK_MSG": "Please enter the task number you want to mark as complete",
        "COMPLETE_TASK_INVALID": "Invalid task number. Please try again later.",
        "COMPLETE_TASK_SUCCESS": "Task #{} '{}' marked as complete successfully.",
        "COMPLETE_TASK_PROBLEM": "Problem with marking task as complete. Please try again later.",
        "LANGUAGE_ASK": (
            "🌐 **Please choose your interface language:**\n"
            "Tap a button below to continue:"
        ),
        "LANGUAGE_OK": (
            "✅ **Language updated successfully!**\n"
            "Let’s keep moving forward together."
        ),
        "LANGUAGE_INVALID": (
            "⚠️ Oops! That’s not a valid option.\n"
            "Please select a language from the list."
        )
    }
}

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
BUTTON_YES: str = "Yes"
BUTTON_NO: str = "No"
BUTTON_DELETE_TASK = "Delete Task"
BUTTON_EDIT_TASK = "Edit Task"
BUTTON_TOGGLE_STATUS = "Complete"
BUTTON_ALL_TASKS = "All tasks"


