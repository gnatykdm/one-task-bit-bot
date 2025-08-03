from typing import Any

MESSAGES: Any = {
    "UKRANIAN": {
        "START_MSG": (
            "🎉 Вітаю, друже! \n"
            "Готовий зарядитися енергією та зробити сьогоднішній день незабутнім? Я тут, щоб допомогти тобі сяяти! 💪"
        ),
        "START_MSG_AGAIN": (
            "👋 З поверненням, чемпіоне! \n"
            "Рокки готовий підтримати тебе на шляху до нових звершень! Твій день — твоя перемога! 🌟"
        ),
        "HELP_MSG": (
            "❓ Трішки заплутався? Не біда! \n"
            "Спробуй /start, /language або /menu — я завжди поруч, щоб підказати! 😊"
        ),
        "MENU_MSG": (
            "📋 Твоє персональне меню готове! \n"
            "Обери, що хочеш, і давай разом економити твій час та натхнення! 💡"
        ),
        "AUTHORIZATION_PROBLEM": (
            "🚫 Ой, здається, потрібен маленький старт! \n"
            "Напиши /start, і ми разом розберемося! 😄"
        ),
        "TEXT_RESPONSE": (
            "✉️ Ти написав: \"{response}\". \n"
            "Дякую, що поділився! Я ціную твої думки! 😊"
        ),
        "CONTINUE_MSG": (
            "✨ Що далі, друже? \n"
            "Відкрий /menu, обери свій шлях, а я підтримаю тебе на кожному кроці! 💪"
        ),
        "SETTINGS_RESPONSE": "⚙️ Заходимо в налаштування... Давай зробимо все по-твоєму! 😊",
        "MYDAY_RESPONSE": "📅 Твій план на сьогодні готовий! Давай зробимо цей день крутим! 🔥",
        "IDEA_RESPONSE": "💡 Є крута ідея? Швидко пиши її — я збережу для тебе! 😊",
        "IDEA_SAVED": "✅ Твоя ідея в безпеці! Ти молодець, що записав! 🌟",
        "ADD_TASK_RESPONSE": "📝 Додаємо нове завдання... Ти на правильному шляху! 😊",
        "IDEA_ACTION": "📌 Що хочеш зробити з цією ідеєю, друже? 😄",
        "IDEA_DELETE": "🗑️ Ідею видалено! Готові до нових? 💪",
        "IDEA_PROBLEM": "⚠️ Ой, щось пішло не так із збереженням ідеї. Спробуй ще раз, я вірю в тебе! 😊",
        "IDEAS_SHOW": "💡 Ось твої круті ідеї, готові до дії! 😄",
        "IDEA_EXISTS": "⚠️ Така ідея вже є! Може, придумаємо щось новеньке? 😊",
        "ERROR_SAVING_IDEA": "⚠️ Щось пішло не так зі збереженням. Спробуй ще раз трішки пізніше! 😌",
        "NO_IDEAS": "📝 Поки ідей немає, але я знаю, що в тебе їх купа! Додай першу! 🚀",
        "DELETE_IDEA": "ℹ️ Назви номер ідеї, яку хочеш видалити, і я все зроблю! 😊",
        "UPDATE_IDEA": "ℹ️ Скажи номер ідеї, яку хочеш оновити, і давай її вдосконалимо! ✏️",
        "NOT_VALID_IDEA_NUM": "❌ Хм, здається, номер не той. Спробуй ще раз! 😄",
        "INVALID_IDEA_NUM": "❌ Ой, неправильний номер! Давай ще раз, ти впораєшся! 😊",
        "IDEA_DELETED": "🗑️ Ідею №{} '{}' видалено! Готові до нових звершень? 💪",
        "ASK_NEW_IDEA_TEXT": "✏️ Напиши новий текст для ідеї №{} '{}', і я оновлю! 😊",
        "IDEA_UPDATED": "✅ Ідея №{} оновлена! Ти круто справляєшся! 🔥",
        "TASK_ADD": "📝 Напиши назву завдання, натисни кнопку, і ми в грі! 😄",
        "TASK_DEADLINE_ASK": "⏰ Хочеш додати дедлайн до завдання? Я поруч! 😊",
        "TASK_DEADLINE_YES": "🕒 Напиши час дедлайну, наприклад, 13:10, і я зафіксую! 😄",
        "TASK_DEADLINE_NO": "✅ Завдання збережено без дедлайну! Ти молодець! 🏆",
        "TASK_DEADLINE_INVALID": "❌ Хм, час неправильний. Спробуй ще раз, я вірю в тебе! 😊",
        "TASK_SAVED": "✅ Завдання в кишені! Ти на висоті! 🎉",
        "TASK_MENU": "📂 Твоє меню завдань — усе під контролем! 😄",
        "NO_TASKS": "❌ Поки завдань немає, але я знаю, що ти готовий їх додати! Спробуй /task! 🚀",
        "YOUR_TASKS": "📋 Ось твої завдання — давай їх розгромимо! 💪",
        "TASK_DELETE_MSG": "🗑️ Назви номер завдання, яке хочеш видалити, і я приберу! 😊",
        "INVALID_TASK_NUM": "❌ Ой, номер не той! Спробуй ще раз! 😄",
        "TASK_DELETED": "✅ Завдання №{} '{}' видалено! Ти крутий! 💥",
        "TASK_DELETE_PROBLEM": "⚠️ Щось пішло не так із видаленням. Спробуй ще раз пізніше! 😌",
        "COMPLETE_TASK_MSG": "✅ Назви номер завдання, яке ти виконав, — відсвяткуємо! 🎉",
        "COMPLETE_TASK_INVALID": "❌ Хм, номер не той. Спробуй ще раз! 😊",
        "COMPLETE_TASK_SUCCESS": "🏆 Завдання №{} '{}' виконано! Ти просто зірка! 🌟",
        "COMPLETE_TASK_PROBLEM": "⚠️ Щось пішло не так із оновленням. Давай ще раз? 😌",
        "UPDATE_TASK_MSG": "✏️ Назви номер завдання для оновлення, і ми його підправимо! 😊",
        "UPDATE_TASK_INVALID": "❌ Неправильний номер. Спробуй ще раз, ти впораєшся! 😄",
        "UPDATE_TASK_SUCCESS": "✅ Завдання №{} оновлено! Ти на висоті! 🔥",
        "UPDATE_TASK_PROBLEM": "⚠️ Щось не так із оновленням. Спробуй ще раз! 😌",
        "UPDATE_TASK_NAME_MSG": "📝 Напиши нову назву завдання, і я оновлю! 😊",
        "UPDATE_TASK_NAME_INVALID": "❌ Назва не підходить. Давай ще раз, я вірю в тебе! 😄",
        "SETTINGS_MENU": "⚙️ Ласкаво просимо до налаштувань! Давай зробимо все зручним для тебе! 😊",
        "ROUTINE_MENU_DAY": "🌅 Хочеш налаштувати ранковий чи вечірній розпорядок? Я з тобою! 😄",
        "MORNING_ROUTINE": "☀️ Твій ранковий розпорядок — заряд на весь день! 💪",
        "EVENING_ROUTINE": "🌙 Твій вечірній розпорядок — час для релаксу! 😊",
        "ROUTINES_INVALID": "❌ Ой, щось пішло не так. Давай спробуємо ще раз? 😌",
        "ADD_MORNING_ROUTINE": "📝 Напиши назву для твого ранкового розпорядку! 😊",
        "INVALID_MORNING_ROUTINE": "❌ Назва не підходить. Спробуй ще раз, я вірю в тебе! 😄",
        "ROUTINE_EXISTS": "⚠️ Такий розпорядок уже є. Може, придумаємо нову назву? 😊",
        "ROUTINE_SAVED": "✅ Розпорядок «{}» готовий! Ти круто справляєшся! 🎉",
        "MORNING_ROUTINE_SHOW": "☀️ Ось твої ранкові розпорядки — готові до дії! 😊",
        "EVENING_ROUTINE_SHOW": "🌙 Твої вечірні розпорядки — час для спокою! 😄",
        "NO_MORNING_ROUTINE": "📝 Ранкового розпорядку ще немає. Давай створимо його разом? 🚀",
        "PROVIDE_ROUTINE_ID": "🔢 Назви номер розпорядку, і я все зроблю! 😊",
        "ROUTINE_DELETED": "🗑️ Розпорядок видалено! Готові до нових ідей? 💪",
        "NEW_ROUTINE_NAME": "✏️ Напиши нову назву для розпорядку! 😊",
        "ROUTINE_NAME_SET": "✅ Назву розпорядку змінено на «{}»! Ти молодець! 🌟",
        "SMTP_MESSAGE_TEXT": "📝 Поділися своїм відгуком — я весь у слухах! 😊",
        "SMTP_MESSAGE_SENT": "🙏 Дякую за твій відгук! Ти допомагаєш нам ставати кращими! 💖",
        "INVALID_MESSAGE": "❌ Текст не підходить. Спробуй ще раз, я вірю в тебе! 😄",
        "SET_TIME_MSG": "⏰ Напиши час для таймера (наприклад, 10:00)! 😊",
        "TIMER_SET": "✅ Таймер на {} встановлено! Ти на правильному шляху! 😄",
        "ROUTINE_TIME": "⏰ Прокидаєшся о {}, лягаєш спати о {}, загальний час дня: {}. Чудовий план! 😊",
        "TIMER_INVALID": "❌ Неправильний формат часу (потрібно 10:00). Спробуй ще раз! 😌",
        "IDEA_EXIST": "⚠️ Ідея з такою назвою вже є. Придумай нову, ти ж креативний! 😊",
        "LANGUAGE_ASK": (
            "🌐 Яку мову обереш, друже? \n"
            "Тисни кнопку нижче, і поїхали! 😄"
        ),
        "LANGUAGE_OK": "✅ Мову змінено! Готові до нових пригод? 🚀",
        "LANGUAGE_INVALID": "⚠️ Щось не те з вибором. Спробуй ще раз, я поруч! 😊"
    },

    "ENGLISH": {
        "START_MSG": (
            "🎉 Hey there, friend! \n"
            "Ready to kick off your day with some energy and good vibes? I’m here to help you shine! 💪"
        ),
        "START_MSG_AGAIN": (
            "👋 Welcome back, champ! \n"
            "Rocky’s here to cheer you on and keep you moving forward! Your day, your victory! 🌟"
        ),
        "HELP_MSG": (
            "❓ Feeling a bit lost? No worries! \n"
            "Try /start, /language, or /menu — I’ve got your back! 😊"
        ),
        "MENU_MSG": (
            "📋 Your personal menu is ready! \n"
            "Pick what you need, and let’s save your time and spark! 💡"
        ),
        "AUTHORIZATION_PROBLEM": (
            "🚫 Oops, looks like we need a quick start! \n"
            "Type /start, and we’ll sort it out together! 😄"
        ),
        "TEXT_RESPONSE": (
            "✉️ You wrote: \"{response}\". \n"
            "Thanks for sharing! I really value your thoughts! 😊"
        ),
        "CONTINUE_MSG": (
            "✨ What’s next, buddy? \n"
            "Open /menu, pick your path, and I’ll be right there with you! 💪"
        ),
        "SETTINGS_RESPONSE": "⚙️ Diving into settings... Let’s make things just right for you! 😊",
        "MYDAY_RESPONSE": "📅 Here’s your plan for today! Let’s make it an awesome day! 🔥",
        "IDEA_RESPONSE": "💡 Got a brilliant idea? Jot it down — I’ll keep it safe for you! 😊",
        "IDEA_SAVED": "✅ Your idea is safe and sound! Nice job writing it down! 🌟",
        "ADD_TASK_RESPONSE": "📝 Adding a new task... You’re on the right track! 😊",
        "IDEA_ACTION": "📌 What do you want to do with this idea, friend? 😄",
        "IDEA_DELETE": "🗑️ Idea deleted! Ready for some fresh ones? 💪",
        "IDEA_PROBLEM": "⚠️ Uh-oh, something went wrong saving your idea. Try again, I believe in you! 😊",
        "IDEAS_SHOW": "💡 Here are your awesome ideas, ready to roll! 😄",
        "IDEA_EXISTS": "⚠️ That idea’s already here! How about something new and exciting? 😊",
        "ERROR_SAVING_IDEA": "⚠️ Something went wrong with saving. Try again a bit later! 😌",
        "NO_IDEAS": "📝 No ideas yet, but I know you’re full of them! Add your first one! 🚀",
        "DELETE_IDEA": "ℹ️ Tell me the idea number to delete, and I’ll take care of it! 😊",
        "UPDATE_IDEA": "ℹ️ Tell me the idea number to update, and let’s make it even better! ✏️",
        "NOT_VALID_IDEA_NUM": "❌ Hmm, that number doesn’t look right. Try again! 😄",
        "INVALID_IDEA_NUM": "❌ Oops, wrong number! Give it another shot, you got this! 😊",
        "IDEA_DELETED": "🗑️ Idea #{} '{}' deleted! Ready for new adventures? 💪",
        "ASK_NEW_IDEA_TEXT": "✏️ Type the new text for idea #{} '{}', and I’ll update it! 😊",
        "IDEA_UPDATED": "✅ Idea #{} updated! You’re killing it! 🔥",
        "TASK_ADD": "📝 Type the task name, hit the button, and we’re in business! 😄",
        "TASK_DEADLINE_ASK": "⏰ Want to add a deadline for this task? I’m here for you! 😊",
        "TASK_DEADLINE_YES": "🕒 Enter the deadline time, like 13:10, and I’ll lock it in! 😄",
        "TASK_DEADLINE_NO": "✅ Task saved without a deadline! You’re awesome! 🏆",
        "TASK_DEADLINE_INVALID": "❌ Hmm, that time doesn’t look right. Try again, I know you can! 😊",
        "TASK_SAVED": "✅ Task saved! You’re on fire! 🎉",
        "TASK_MENU": "📂 Your task menu — everything’s under control! 😄",
        "NO_TASKS": "❌ No tasks yet, but I know you’re ready to add some! Try /task! 🚀",
        "YOUR_TASKS": "📋 Here are your tasks — let’s crush them! 💪",
        "TASK_DELETE_MSG": "🗑️ Tell me the task number to delete, and I’ll handle it! 😊",
        "INVALID_TASK_NUM": "❌ Oops, wrong number! Try again! 😄",
        "TASK_DELETED": "✅ Task #{} '{}' deleted! You’re rocking it! 💥",
        "TASK_DELETE_PROBLEM": "⚠️ Something went wrong with deleting. Try again later! 😌",
        "COMPLETE_TASK_MSG": "✅ Tell me the number of the task you nailed — let’s celebrate! 🎉",
        "COMPLETE_TASK_INVALID": "❌ Hmm, that number’s off. Try again! 😊",
        "COMPLETE_TASK_SUCCESS": "🏆 Task #{} '{}' done! You’re absolutely crushing it! 🌟",
        "COMPLETE_TASK_PROBLEM": "⚠️ Something went wrong with updating. Wanna try again? 😌",
        "UPDATE_TASK_MSG": "✏️ Tell me the task number to update, and we’ll tweak it! 😊",
        "UPDATE_TASK_INVALID": "❌ Wrong number! Try again, you got this! 😄",
        "UPDATE_TASK_SUCCESS": "✅ Task #{} updated! You’re on a roll! 🔥",
        "UPDATE_TASK_PROBLEM": "⚠️ Something went wrong with updating. Try again soon! 😌",
        "UPDATE_TASK_NAME_MSG": "📝 Type the new task name, and I’ll update it! 😊",
        "UPDATE_TASK_NAME_INVALID": "❌ That name doesn’t work. Try again, I believe in you! 😄",
        "SETTINGS_MENU": "⚙️ Welcome to settings! Let’s make everything perfect for you! 😊",
        "ROUTINE_MENU_DAY": "🌅 Want to set up a morning or evening routine? I’m with you! 😄",
        "MORNING_ROUTINE": "☀️ Your morning routine — ready to start the day strong! 💪",
        "EVENING_ROUTINE": "🌙 Your evening routine — time to unwind! 😊",
        "ROUTINES_INVALID": "❌ Oops, something went wrong. Shall we try again? 😌",
        "ADD_MORNING_ROUTINE": "📝 Type a title for your morning routine! 😊",
        "INVALID_MORNING_ROUTINE": "❌ That title doesn’t work. Try another, you got this! 😄",
        "ROUTINE_EXISTS": "⚠️ A routine with that title already exists. How about a new one? 😊",
        "ROUTINE_SAVED": "✅ Routine «{}» saved! You’re doing awesome! 🎉",
        "MORNING_ROUTINE_SHOW": "☀️ Your morning routines, ready to kickstart your day! 😊",
        "EVENING_ROUTINE_SHOW": "🌙 Your evening routines — perfect for winding down! 😄",
        "NO_MORNING_ROUTINE": "📝 No morning routine yet. Let’s create one together? 🚀",
        "PROVIDE_ROUTINE_ID": "🔢 Tell me the routine number, and I’ll take care of it! 😊",
        "ROUTINE_DELETED": "🗑️ Routine deleted! Ready for new plans? 💪",
        "NEW_ROUTINE_NAME": "✏️ Type a new name for the routine! 😊",
        "ROUTINE_NAME_SET": "✅ Routine name changed to «{}». You’re killing it! 🌟",
        "SMTP_MESSAGE_TEXT": "📝 Share your feedback — I’m all ears! 😊",
        "SMTP_MESSAGE_SENT": "🙏 Thanks for your feedback! You’re helping us get better! 💖",
        "INVALID_MESSAGE": "❌ That text doesn’t work. Try again, I know you can! 😄",
        "SET_TIME_MSG": "⏰ Enter the time for your timer (like 10:00)! 😊",
        "TIMER_SET": "✅ Timer set for {}! You’re on the right track! 😄",
        "TIMER_INVALID": "❌ Wrong time format (use 10:00). Try again! 😌",
        "ROUTINE_TIME": "⏰ Wake up at {}, sleep at {}, total day time: {}. Great plan! 😊",
        "IDEA_EXIST": "⚠️ An idea with that name already exists. Got another creative one? 😊",
        "LANGUAGE_ASK": (
            "🌐 What language would you like, friend? \n"
            "Pick one below, and let’s roll! 😄"
        ),
        "LANGUAGE_OK": "✅ Language updated! Ready for new adventures? 🚀",
        "LANGUAGE_INVALID": "⚠️ Something’s off with that choice. Try again, I’m here! 😊"
    }
}

# Buttons
BUTTON_ADD_TASK: str = "📝 Add a Task"
BUTTON_IDEA: str = "💾 Save an Idea"
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

USER_FEEDBACK_MAIL_TEXT = """
📬 Hey, we’ve got new feedback!

Here’s what our awesome user shared:

------------------------
{feedback}
------------------------

🧑‍💻 User Details:
- Username: {username}
- User ID: {user_id}
- Date: {date}

Let’s take a look and make things even better!
"""

def generate_daily_stats_message(language: str, created_ideas: int, completed_tasks: int, created_tasks: int) -> str:
    lang = language.upper()
    if lang == "UKRANIAN":
        return (
            "📊 *Твоя щоденна статистика, друже!*\n\n"
            f"🧠 *Створено ідей*: {created_ideas}\n"
            f"✅ *Виконано завдань*: {completed_tasks}\n"
            f"📝 *Додано завдань*: {created_tasks}\n\n"
            "🔄 Оновлюється щодня о 00:00.\n\n"
            "Ти просто зірка, так тримати! 🌟"
        )
    else:
        return (
            "📊 *Your Daily Stats, Champ!*\n\n"
            f"🧠 *Ideas created*: {created_ideas}\n"
            f"✅ *Tasks completed*: {completed_tasks}\n"
            f"📝 *Tasks added*: {created_tasks}\n\n"
            "🔄 Updates every day at 00:00.\n\n"
            "You’re absolutely crushing it! Keep shining! 🌟"
        )