from typing import Any

MESSAGES: Any = {
    "UKRANIAN": {
        "START_MSG": "🎉 Ласкаво просимо до бота!\nГотові почати новий продуктивний день?",
        "START_MSG_AGAIN": "👋 З поверненням, чемпіоне!\nРадий вас бачити знову 😊",
        "HELP_MSG": "ℹ️ Потрібна допомога?\nВикористовуйте /start, /language або /menu, щоб знайти потрібне 📋",
        "MENU_MSG": "📋 **Ваше меню:**\nОбирайте дію нижче 👇",
        "AUTHORIZATION_PROBLEM": "🚫 Упс, ви не авторизовані.\nБудь ласка, спробуйте /start, щоб почати.",
        "TEXT_RESPONSE": "✉️ Ви написали: \"{response}\".\nДякую за повідомлення! 🙌",
        "CONTINUE_MSG": "✨ Чим ще можу допомогти?\nСміливо користуйтесь /menu для всіх можливостей 🌟",
        "SETTINGS_RESPONSE": "🔧 Відкриваю налаштування...",
        "MYDAY_RESPONSE": "📅 Ось ваш план на сьогодні...",
        "IDEA_RESPONSE": "💡 Поділіться своєю ідеєю, я все запишу!",
        "IDEA_SAVED": "💡 Ідея успішно збережена.",
        "ADD_TASK_RESPONSE": "📝 Створюємо нову задачу...",
        "LANGUAGE_ASK": (
            "🌐 **Оберіть мову інтерфейсу:**\n"
            "Натисніть кнопку нижче, щоб продовжити:"
        ),
        "LANGUAGE_OK": (
            "✅ **Мову оновлено!**\n"
            "Продовжуємо працювати разом."
        ),
        "LANGUAGE_INVALID": (
            "⚠️ Упс! Це недійсний варіант.\n"
            "Будь ласка, оберіть мову зі списку."
        )
    },
    "ENGLISH": {
        "START_MSG": "🎉 Welcome to the bot!\nReady to kick off a productive day?",
        "START_MSG_AGAIN": "👋 Welcome back, legend!\nHappy to see you again 😊",
        "HELP_MSG": "ℹ️ Need some help?\nUse /start, /language, or /menu to get around 📋",
        "MENU_MSG": "📋 **Your menu:**\nPick what you’d like to do 👇",
        "AUTHORIZATION_PROBLEM": "🚫 Oops! You’re not authorized.\nPlease use /start to begin.",
        "TEXT_RESPONSE": "✉️ You wrote: \"{response}\".\nThanks for sharing! 🙌",
        "CONTINUE_MSG": "✨ What else can I help you with?\nUse /menu to explore all options 🌟",
        "SETTINGS_RESPONSE": "🔧 Opening your settings...",
        "MYDAY_RESPONSE": "📅 Here’s your plan for today...",
        "IDEA_RESPONSE": "💡 Tell me your idea, I’ll save it for you!",
        "IDEA_SAVED": "💡 Idea saved successfully.",
        "ADD_TASK_RESPONSE": "📝 Creating a new task...",
        "LANGUAGE_ASK": (
            "🌐 **Choose your language:**\n"
            "Tap a button below to continue:"
        ),
        "LANGUAGE_OK": (
            "✅ **Language updated!**\n"
            "Let’s keep moving forward."
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