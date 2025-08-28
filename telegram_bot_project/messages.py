# messages.py
from typing import Any
from aiogram import Bot
from service.user import UserService
from service.routine import RoutineService

MESSAGES: Any = {
    "UKRANIAN": {
        "START_MSG": (
            "🎉 Вітаємо!\n\n"
            "Я — Роккі, твій персональний помічник для організації дня.\n"
            "Зі мною ти зможеш створювати завдання, отримувати нагадування в потрібний час і ефективно планувати свій день.\n"
            "Я допоможу слідкувати за важливими справами та не забути про головне.\n"
            "Просто почни додавати завдання, і Роккі буде стежити за їх виконанням!"
        ),
        "START_MSG_AGAIN": (
            "👋 Ви повернулися! \n"
            "Обирайте дію через /menu."
        ),
        "HELP_MSG": (
            "❓ Потрібна допомога? \n"
            "Використовуйте /start, /language або /menu для навігації."
        ),
        "MENU_MSG": (
            "📋 Ось ваше меню. \n"
            "Виберіть потрібну опцію для продовження."
        ),
        "AUTHORIZATION_PROBLEM": (
            "🚫 Виникла проблема з авторизацією. \n"
            "Спробуйте /start для початку."
        ),
        "TEXT_RESPONSE": (
            "✉️ Отримано: \"{response}\". \n"
            "Дякуємо за ваш ввід!"
        ),
        "CONTINUE_MSG": (
            "➡️ Що далі? \n"
            "Відкрийте /menu, щоб обрати наступну дію."
        ),
        "SETTINGS_RESPONSE": "⚙️ Відкриваємо налаштування. Давайте налаштуємо все під вас.",
        "MYDAY_RESPONSE": "📅 Ваш план на день готовий. Перегляньте його!",
        "IDEA_RESPONSE": "💡 Маєте нотатка? Напишіть, я збережу її.",
        "IDEA_SAVED": "✅ Нотатку збережено. Дякуємо за внесок!",
        "ADD_TASK_RESPONSE": "📝 Додаємо завдання. Вкажіть деталі.",
        "IDEA_ACTION": "📌 Що зробити з цією нотаткою? Виберіть дію.",
        "IDEA_DELETE": "🗑️ Нотатку видалено. Готові до нових?",
        "IDEA_PROBLEM": "⚠️ Помилка збереження нотатки. Спробуйте ще раз.",
        "IDEAS_SHOW": "💡 Ваші нотатки готові до перегляду.",
        "IDEA_EXISTS": "⚠️ Нотатка вже існує. Спробуйте нову.",
        "ERROR_SAVING_IDEA": "⚠️ Не вдалося зберегти нотатку. Спробуйте пізніше.",
        "NO_IDEAS": "📝 Нотатку поки немає. Додайте першу!",
        "DELETE_IDEA": "ℹ️ Вкажіть номер нотатки для видалення.",
        "UPDATE_IDEA": "ℹ️ Вкажіть номер нотатки для оновлення.",
        "NOT_VALID_IDEA_NUM": "❌ Неправильний номер нотатки. Спробуйте ще раз.",
        "INVALID_IDEA_NUM": "❌ Номер нотатки некоректний. Перевірте ще раз.",
        "IDEA_DELETED": "🗑️ Нотатка №{} '{}' видалена. Готові до нових завдань?",
        "ASK_NEW_IDEA_TEXT": "✏️ Введіть новий текст для нотатки №{} '{}'.",
        "IDEA_UPDATED": "✅ Нотатка №{} оновлена. Відмінна робота!",
        "TASK_ADD": "📝 Вкажіть назву завдання для додавання.",
        "TASK_DEADLINE_ASK": "⏰ Додати дедлайн до завдання? Виберіть опцію.",
        "TASK_DEADLINE_YES": "🕒 Введіть час дедлайну (наприклад, 13:10).",
        "TASK_DEADLINE_NO": "✅ Завдання збережено без дедлайну.",
        "TASK_DEADLINE_INVALID": "❌ Некоректний формат часу. Спробуйте ще раз.",
        "TASK_SAVED": "✅ Завдання збережено. Продовжуйте!",
        "TASK_MENU": "📂 Меню завдань. Усе під контролем.",
        "NO_TASKS": "❌ Завдань поки немає.\nДодайте нове через /task",
        "YOUR_TASKS": "📋 Список ваших завдань",
        "TASK_DELETE_MSG": "🗑️ Вкажіть номер завдання для видалення.",
        "INVALID_TASK_NUM": "❌ Некоректний номер завдання.\nСпробуйте ще раз. 🔢",
        "TASK_DELETED": "✅ Завдання №{} '{}' видалено.",
        "TASK_DELETE_PROBLEM": "⚠️ Помилка видалення завдання.\nСпробуйте пізніше. ⏳",
        "COMPLETE_TASK_MSG": "✅ Вкажіть номер завершеного завдання. 🏆",
        "COMPLETE_TASK_INVALID": "❌ Некоректний номер завдання.\nСпробуйте ще раз. 🔢",
        "COMPLETE_TASK_SUCCESS": "🏆 Завдання №{} '{}' виконано.\nВідмінно! 📝",
        "COMPLETE_TASK_PROBLEM": "⚠️ Помилка оновлення завдання.\nСпробуйте ще раз. 🔄",
        "UPDATE_TASK_MSG": "✏️ Вкажіть номер завдання для оновлення. 📝",
        "UPDATE_TASK_INVALID": "❌ Некоректний номер завдання.\nСпробуйте ще раз. 🔢",
        "UPDATE_TASK_SUCCESS": "✅ Завдання №{} оновлено.\nГарна робота! 📝",
        "UPDATE_TASK_PROBLEM": "⚠️ Помилка оновлення завдання.\nСпробуйте пізніше. ⏳",
        "UPDATE_TASK_NAME_MSG": "📝 Введіть нову назву завдання.\n🛠️",
        "UPDATE_TASK_NAME_INVALID": "❌ Некоректна назва завдання.\nСпробуйте ще раз. 🔢",
        "SETTINGS_MENU": "⚙️ Меню налаштувань. Налаштуйте все за вашим бажанням.",
        "ROUTINE_MENU_DAY": "🌅 Налаштувати ранковий чи вечірній розпорядок?",
        "MORNING_ROUTINE": "☀️ Ваш ранковий розпорядок готовий.",
        "EVENING_ROUTINE": "🌙 Ваш вечірній розпорядок готовий.",
        "ROUTINES_INVALID": "❌ Помилка з розпорядками.\nСпробуйте ще раз. 🔄",
        "ADD_MORNING_ROUTINE": "📝 Введіть назву для ранкового розпорядку.",
        "INVALID_MORNING_ROUTINE": "❌ Некоректна назва.\nСпробуйте ще раз. 🔢",
        "ROUTINE_EXISTS": "⚠️ Розпорядок з такою назвою вже існує.\nВиберіть іншу. 📝",
        "ROUTINE_SAVED": "✅ Розпорядок «{}» збережено.",
        "MORNING_ROUTINE_SHOW": "☀️ Ваші ранкові розпорядки:",
        "EVENING_ROUTINE_SHOW": "🌙 Ваші вечірні розпорядки:",
        "NO_MORNING_ROUTINE": "📝 Ранкових розпорядків немає. Додайте перший!",
        "NO_EVENING_ROUTINE": "📝 Вечірних розпорядків немає. Додайте перший!",
        "ROUTINE_TIME_NOT": "⚠️ Ви ще не маєте налаштованих годин пробудження і сну.",
        "PROVIDE_ROUTINE_ID": "🔢 Вкажіть номер розпорядку для дії.",
        "ROUTINE_DELETED": "🗑️ Розпорядок видалено.",
        "NEW_ROUTINE_NAME": "✏️ Введіть нову назву розпорядку.",
        "ROUTINE_NAME_SET": "✅ Назва розпорядку змінена на «{}».",
        "SMTP_MESSAGE_TEXT": "📝 Напишіть ваш відгук.\nМи цінуємо вашу думку! 💬",
        "SMTP_MESSAGE_SENT": "🙏 Відгук отримано.\nДякуємо за ваш внесок! 📝",
        "INVALID_MESSAGE": "❌ Некоректний текст.\nСпробуйте ще раз. 🔢",
        "SET_TIME_MSG": "⏰ Введіть час для таймера (наприклад, 10:00).",
        "TIMER_SET": "✅ Таймер встановлено на {}.",
        "ROUTINE_TIME": "🌅 Прокидання: {wake}\n🌙 Сон: {sleep}\n⏳ Тривалість дня: {duration}",
        "TIMER_INVALID": "❌ Некоректний формат часу (потрібно 10:00). Спробуйте ще раз.",
        "IDEA_EXIST": "⚠️ Нотатка з такою назвою вже існує.",
        "SEND_MORNING_MSG": "Твій ранковий розпорядок ☀️:\n",
        "SEND_EVENING_MSG": "🌙 Доброго вечора, {}!",
        "WELCOME_TO_FOCUS": "🎯 Вітаємо у зоні фокусу!",
        "START_FOCUS_MSG": "Сесію фокусу розпочато. 🕒",
        "STOP_FOCUS_MSG": "Сесію фокусу зупинено.\n⏳ Тривалість: - {}хв {}с.",
        "SAVE_FOCUS_ZONE": "❗ Зберегти сесію фокусу?",
        "SAVED_FOCUS_MSG": "Сесію фокусу збережено. ✅",
        "NOT_SAVED_FOCUS_MSG": "Сесію фокусу не збережено. ❌",
        "TITLE_FOCUS_ZONE_MSG": "Бажаєте дати назву цій сесії? 📝",
        "NOT_FOUND_FOCUS_SESSION": "❗ Не знайдено початку фокус-сесії.",
        "FOCUS_INVALID": "❗ Неправильний параметр фокусування",
        "FOCUS_TITLE_ASK": "✏️ Будь ласка, введіть назву фокус-сесії.",
        "FOCUS_EXISTS": "❗ Фокус-сесія вже активна.",
        "FOCUS_LIST_TITLE": "🧠 Список ваших фокус-сесій",
        "NO_FOCUS_SESSIONS": "😕 У вас ще немає жодної фокус-сесії.",
        "LANGUAGE_ASK": (
            "🌐 Виберіть мову для роботи. \n"
            "Оберіть опцію нижче. 📚"
        ),
        "LANGUAGE_OK": "✅ Мову змінено.\nГотові продовжити? 🚀",
        "LANGUAGE_INVALID": "❌ Некоректний вибір мови.\nСпробуйте ще раз. 🔢",
        "DELETE_FOCUS_SESSION_MSG": "🔢 Вкажіть номер сесії, яку ви хочете видалити.",
        "FOCUS_DELETED": "✅ Фокус-сесію №{} з назвою \"{}\" успішно видалено.",
        "REMIND_WORK_CANCEL": "✅ Нагадування для цього завдання було вимкнено",
        "REMIND_WORK_START": "⏰ Увага! Завдання *{}* починається — час діяти!",
        "FINISH_WORK_SESSION": "🎉 Вітаємо, ви виконали завдання - {}\n⏳ Час, витрачений на завдання: {}хв {}с\nПродовжуйте в тому ж дусі! 🏆",
        "BREAK_WORK_SESSION": "✅ Ви успішно зробили перерву в робочій сесії.\nЗакінчіть її, коли знайдете час :)",
        "WAKE_UP_MESSAGE": "☀️ Доброго ранку, {}! Час прокидатися та розпочати свій день.",
        "MORNING_TASK_CREATE_MSG": "Гарного дня!\nНе забудь скласти завдання на сьогодні. /task 📝",
        "MORNING_ROUTINE_TIMES_START": "🕒 Таймер ранкової рутини увімкнено.",
        "MORNING_TASK_CREATE_TIMER_MSG": "Гарного дня!\n🕒 Час на виконання ранкової рутини: {}m {}s\nНе забудь скласти завдання на сьогодні. /task 📝",
        "AI_ROCKY_TALK_MSG": "Привіт, {} 👋\nЧим я можу допомогти тобі сьогодні❓",
        "AI_ROCKY_TALK_END_MSG": "Було приємно поспілкуватися з тобою, {} ✨\nБажаю чудового дня! 🌿",
        "CURRENT_TIMEZONE": "Ваш поточний часовий пояс:\n🕒 {}",
        "TIMEZONE_SWITCHED_OK": "✅ Часовий пояс успішно змінено",
        "TIMEZONE_BTN_MSG": "ℹ️ Будь ласка, натисніть кнопку, щоб змінити часовий пояс"
    },
    "ENGLISH": {
        "START_MSG": (
            "🎉 Welcome!\n\n"
            "I’m Rocky, your personal assistant for organizing your day.\n"
            "With me, you can create tasks, receive reminders at the right time, and plan your day effectively.\n"
            "I’ll help you keep track of important things and make sure you don’t forget what matters most.\n"
            "Just start adding tasks, and Rocky will take care of the rest!"
        ),
        "START_MSG_AGAIN": (
            "👋 You’re back! \n"
            "Use /menu to choose an action."
        ),
        "HELP_MSG": (
            "❓ Need assistance? \n"
            "Try /start, /language, or /menu to navigate."
        ),
        "MENU_MSG": (
            "📋 Your menu is ready. \n"
            "Select an option to proceed."
        ),
        "AUTHORIZATION_PROBLEM": (
            "🚫 Authorization issue detected. \n"
            "Try /start to begin. 🔄"
        ),
        "TEXT_RESPONSE": (
            "✉️ Received: \"{response}\". \n"
            "Thank you for your input!"
        ),
        "CONTINUE_MSG": (
            "➡️ What’s next? \n"
            "Open /menu to select your next action."
        ),
        "SETTINGS_RESPONSE": "⚙️ Accessing settings. Let’s customize your experience.",
        "MYDAY_RESPONSE": "📅 Your daily plan is ready. Review it now!",
        "IDEA_RESPONSE": "💡 Have an note? Write it down, and I’ll save it.",
        "IDEA_SAVED": "✅ Note saved. Thank you for sharing!",
        "ADD_TASK_RESPONSE": "📝 Adding a task. Provide the details.",
        "IDEA_ACTION": "📌 What would you like to do with this note? Select an action.",
        "IDEA_DELETE": "🗑️ Note deleted. Ready for new ones? ",
        "IDEA_PROBLEM": "⚠️ Error saving the note. Please try again.",
        "IDEAS_SHOW": "💡 Your notes are ready to view.",
        "IDEA_EXISTS": "⚠️ This note already exists. Try a new one.",
        "ERROR_SAVING_IDEA": "⚠️ Failed to save the note. Try again later.",
        "NO_IDEAS": "📝 No notes yet. Add your first one!",
        "DELETE_IDEA": "ℹ️ Specify the note number to delete.",
        "UPDATE_IDEA": "ℹ️ Specify the note number to update.",
        "NOT_VALID_IDEA_NUM": "❌ Invalid note number. Try again.",
        "INVALID_IDEA_NUM": "❌ Incorrect note number. Please check again.",
        "IDEA_DELETED": "🗑️ Note #{} '{}' deleted. Ready for new tasks?",
        "ASK_NEW_IDEA_TEXT": "✏️ Enter new text for note #{} '{}'.",
        "IDEA_UPDATED": "✅ Note #{} updated. Great work!",
        "TASK_ADD": "📝 Enter the task name to add.",
        "TASK_DEADLINE_ASK": "⏰ Add a deadline for this task? Choose an option.",
        "TASK_DEADLINE_YES": "🕒 Enter the deadline time (e.g., 13:10).",
        "TASK_DEADLINE_NO": "✅ Task saved without a deadline.",
        "TASK_DEADLINE_INVALID": "❌ Invalid time format. Try again.",
        "TASK_SAVED": "✅ Task saved. Keep it up!",
        "TASK_MENU": "📂 Task menu. Everything is under control.",
        "NO_TASKS": "❌ No tasks yet. Add one with /task.",
        "YOUR_TASKS": "📋 List of your tasks. Choose one:",
        "TASK_DELETE_MSG": "🗑️ Specify the task number to delete.",
        "INVALID_TASK_NUM": "❌ Incorrect task number. Try again.",
        "TASK_DELETED": "✅ Task #{} '{}' deleted.",
        "TASK_DELETE_PROBLEM": "⚠️ Error deleting task. Try again later.",
        "COMPLETE_TASK_MSG": "✅ Specify the completed task number.",
        "COMPLETE_TASK_INVALID": "❌ Incorrect task number. Try again.",
        "COMPLETE_TASK_SUCCESS": "🏆 Task #{} '{}' completed. Well done!",
        "COMPLETE_TASK_PROBLEM": "⚠️ Error updating task. Try again.",
        "UPDATE_TASK_MSG": "✏️ Specify the task number to update.",
        "UPDATE_TASK_INVALID": "❌ Incorrect task number. Try again.",
        "UPDATE_TASK_SUCCESS": "✅ Task #{} updated. Nice job!",
        "UPDATE_TASK_PROBLEM": "⚠️ Error updating task. Try again later.",
        "UPDATE_TASK_NAME_MSG": "📝 Enter the new task name.",
        "UPDATE_TASK_NAME_INVALID": "❌ Invalid task name.\nTry again.",
        "SETTINGS_MENU": "⚙️ Settings menu. Customize as needed.",
        "ROUTINE_MENU_DAY": "🌅 Set up a morning or evening routine?",
        "MORNING_ROUTINE": "☀️ Your morning routine is ready.",
        "EVENING_ROUTINE": "🌙 Your evening routine is ready.",
        "ROUTINES_INVALID": "❌ Error with routines. Try again.",
        "ADD_MORNING_ROUTINE": "📝 Enter a title for your morning routine.",
        "INVALID_MORNING_ROUTINE": "❌ Invalid title. Try again.",
        "ROUTINE_EXISTS": "⚠️ Routine with this title already exists. Choose another.",
        "ROUTINE_SAVED": "✅ Routine «{}» saved.",
        "MORNING_ROUTINE_SHOW": "☀️ Your morning routines:",
        "EVENING_ROUTINE_SHOW": "🌙 Your evening routines:",
        "NO_MORNING_ROUTINE": "📝 No morning routines yet. Add one!",
        "NO_EVENING_ROUTINE": "📝 No evening routines yet. Add the first one!",
        "PROVIDE_ROUTINE_ID": "🔢 Specify the routine number for action.",
        "ROUTINE_DELETED": "🗑️ Routine deleted. Ready for new plans?",
        "NEW_ROUTINE_NAME": "✏️ Enter a new name for the routine.",
        "ROUTINE_NAME_SET": "✅ Routine name changed to «{}».",
        "ROUTINE_TIME_NOT": "You don’t have wake-up and sleep times set yet.",
        "SMTP_MESSAGE_TEXT": "📝 Share your feedback. We value your input!",
        "SMTP_MESSAGE_SENT": "🙏 Feedback received. Thank you!",
        "INVALID_MESSAGE": "❌ Invalid text. Try again.",
        "SET_TIME_MSG": "⏰ Enter the timer time (e.g., 10:00).",
        "TIMER_SET": "✅ Timer set for {}.",
        "TIMER_INVALID": "❌ Invalid time format (use 10:00). Try again.",
        "ROUTINE_TIME": "⏰ Wake up: {wake}\n😴 Sleep: {sleep}\n⏳ Total day time: {duration}",
        "IDEA_EXIST": "⚠️ Note with this name already exists. Choose another.",
        "SEND_MORNING_MSG": "Your morning routine ☀️:\n",
        "SEND_EVENING_MSG": "🌙 Good evening, {}!",
        "WELCOME_TO_FOCUS": "🎯 Welcome to the focus zone!",
        "START_FOCUS_MSG": "🕒 Focus session started.",
        "STOP_FOCUS_MSG": "Focus session stopped.\n⏳ Duration - {}m {}s.",
        "SAVE_FOCUS_ZONE": "📝 Save the focus session? ",
        "SAVED_FOCUS_MSG": "Focus session saved. ✅",
        "NOT_SAVED_FOCUS_MSG": "Focus session not saved. ❌",
        "TITLE_FOCUS_ZONE_MSG": "Would you like to name this session? 📝",
        "NOT_FOUND_FOCUS_SESSION": "❗ Focus session start not found.",
        "FOCUS_INVALID": "⚠️ Invalid option for focus",
        "FOCUS_TITLE_ASK": "✏️ Please provide the title for focus session.",
        "FOCUS_EXISTS": "❗ A focus session is already active.",
        "FOCUS_LIST_TITLE": "🧠 Your Focus Sessions",
        "NO_FOCUS_SESSIONS": "😕 No focus sessions found.",
        "DELETE_FOCUS_SESSION_MSG": "Provide a number of session which you want to delete.",
        "REMIND_WORK_CANCEL": "✅ Reminders for this task was deactivated",
        "REMIND_WORK_START": "⏰ Heads up! Task *{}* is starting — make it count!",
        "FINISH_WORK_SESSION": "🎉 Congratulations you done task - '{}'.\n⏳ Time duration for this task was: {}m:{}s\nKeep going 🏆! ",
        "BREAK_WORK_SESSION": "✅ You succesfully break the work session.\nComplete it when you will find the time :)",
        "LANGUAGE_ASK": (
            "🌐 Choose your language. \n"
            "Select an option below. 📚"
        ),
        "LANGUAGE_OK": "✅ Language updated. Ready to proceed? 🚀",
        "LANGUAGE_INVALID": "❌ Invalid language choice. Try again. 🔢",
        "FOCUS_DELETED": "✅ Focus session #{} with the title \"{}\" has been successfully deleted.",
        "WAKE_UP_MESSAGE": "☀️ Good morning, {}! Time to wake up and start your day.",
        "MORNING_TASK_CREATE_MSG": "Have a nice day!\nDon't forget to plan your tasks today. /task 📝",
        "MORNING_ROUTINE_TIMES_START": "🕒 Morning routine times is turn on.",
        "MORNING_TASK_CREATE_TIMER_MSG": "Have a nice day!\n🕒 Your working routine duration was: {}m {}s\nDon't forget to plan your tasks today. /task 📝",
        "AI_ROCKY_TALK_MSG": "Hello, {} 👋\nHow i can help you today❓",
        "AI_ROCKY_TALK_END_MSG": "It was nice talking to you, {} ✨\nHave a wonderful day ahead! 🌿",
        "CURRENT_TIMEZONE": "You current timezone is:\n🕒 {}",
        "TIMEZONE_SWITCHED_OK": "✅ Timezone switched successfully",
        "TIMEZONE_BTN_MSG": "ℹ️ Please press the button to switch timezone",
    }
}

# Buttons
BUTTON_SETTINGS = "⬅️ Settings"
BUTTON_ADD_TASK: str = "🆕 Add Task"
BUTTON_IDEA: str = "✏️ Note"
BUTTON_MYDAY: str = "📅 My Day"
BUTTON_HELP: str = "❓ Help"
BUTTON_UA_LANG: str = "🇺🇦 Українська"
BUTTON_EN_LANG: str = "🇬🇧 English"
DEL_BUTTON: str = "🗑️ Remove Note"
DEL_IDEA_BUTTON: str = "🗑️ Delete Note"
SAVE_BUTTON: str = "✅ Save"
MENU_BUTTON: str = "🏠 Main Menu"
UPDATE_IDEA_BUTTON: str = "🆙 Update Note"
ALL_IDEAS: str = "🔍 View All Notes"
BUTTON_YES_BTN: str = "👍 Yes"
BUTTON_NO_BTN: str = "🙅 No"
BUTTON_DELETE_TASK = "🗑️ Delete Task"
BUTTON_EDIT_TASK = "✏️ Edit Task"
BUTTON_TOGGLE_STATUS = "✅ Mark Complete"
BUTTON_ALL_TASKS = "📋 All Tasks"
SETTINGS_BUTTON_LANGUAGE = "🌐 Language"
SETTINGS_BUTTON_FEEDBACK = "💬 Feedback"
SETTINGS_BUTTON_ROUTINE = "📅 Daily Routine"
SETTINGS_BUTTON_ROUTINE_TIME = "⏳ Bedtime & Wake Up"
ROUTINE_SET_WAKE_BUTTON = "⏰ Set Wake-Up Time"
ROUTINE_SET_SLEEP_BUTTON = "🛌 Set Sleep Time"
TIME_ZONE_BTN = "ℹ️ Time zone"
CHANGE_TIMEZONE_BTN = "🌐 Switch Time Zone"
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
FOCUS_INLINE_YES = "✅ Yes"
FOCUS_INLINE_NO = "❌ No"
ALL_FOCUSES_BTN = "📝 All Focuses"
DELETE_FOCUS = "🗑️ Delete"

FOCUS_CALL_BTN = "🎯 Focus"
START_WORK_BTN = "✅ Start"
CANCEL_WORK_BTN = "❌ Cancel"

START_DAY_BTN = "🚀 Start Day"

STOP_WORK_SESSION = "✅ Finished"
STOP_WORK_CANCEL = "❌ Break Work Session"

MORNING_ROUTINE_TIMER_START_BTN = "🟢 Start routine timer"
MORNING_ROUTINE_TIMER_NOPE_BTN = "🔴 Nope"

STOP_ROUTINE_TIMER_BTN = "🔴 Stop routine timer"

AI_ROCKY_BTN = "🤖 AI Rocky"
STOP_CHAT = "❌ Stop"

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

def generate_daily_stats_message(language: str, created_ideas: int, completed_tasks: int, created_tasks: int, wake_up_time: str = None) -> str:
    lang = language.upper()
    if lang == "UKRANIAN":
        return (
            "📊 *Твоя щоденна статистика*:\n\n"
            f"⏰ Час пробудження: *{wake_up_time if wake_up_time else '—'}*\n"
            f"📝 Нотаток створено: *{created_ideas}*\n"
            f"🚀 Завдань додано: *{created_tasks}*\n"
            f"✅ Завдань виконано: *{completed_tasks}*\n\n"
            "🔄 Статистика оновлюється щодня опівночі.\n"
            "✨ Продовжуй рухатися до своїх цілей!"
        )
    else:
        return (
            "📊 *Your Daily Stats*:\n\n"
            f"⏰ Wake-up time: *{wake_up_time if wake_up_time else '—'}*\n"
            f"📝 Notes created: *{created_ideas}*\n"
            f"🚀 Tasks added: *{created_tasks}*\n"
            f"✅ Tasks completed: *{completed_tasks}*\n\n"
            "🔄 Stats refresh daily at midnight.\n"
            "✨ Keep pushing towards your goals!"
        )
