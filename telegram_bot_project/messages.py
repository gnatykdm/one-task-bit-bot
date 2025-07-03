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

BUTTON_ADD_TASK: str = "➕ Add Task"
BUTTON_IDEA: str = "💡 Save Idea"
BUTTON_MYDAY: str = "📅 My Day"
BUTTON_SETTINGS: str = "⚙️ Settings"
BUTTON_HELP: str = "❓ Help"
BUTTON_UA_LANG: str = "🇺🇦 Ukrainian"
BUTTON_EN_LANG: str = "🇬🇧 English"
DEL_BUTTON: str = "🗑️ Delete"
SAVE_BUTTON: str = "💾 Save"
