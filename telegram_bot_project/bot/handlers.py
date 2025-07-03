from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons import get_idea_conf_keyboard, menu_reply_keyboard
from messages import MESSAGES
from service.idea import IdeaService
from service.user import UserService

async def process_idea_save(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    if not user_find or not user_find.get("id"):
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    language = await UserService.get_user_language(user_id) or "ENGLISH"
    idea = message.text.strip()

    exist = await IdeaService.get_by_idea_name(idea)
    if exist:
        await message.answer(
            MESSAGES[language].get('IDEA_EXIST', "⚠️ This idea already exists."),
            reply_markup=menu_reply_keyboard()
        )
        return

    print(f"--[INFO] User with id: {user_id} provided idea.")

    try:
        await state.update_data(idea=idea)

        divider = "\n" + ("-" * int(len(MESSAGES[language]['IDEA_ACTION']) * 1.65))

        keyboard = get_idea_conf_keyboard()

        await message.answer(
            f"{MESSAGES[language]['IDEA_ACTION']}{divider}\n💡 *Idea:* {idea}",
            reply_markup=keyboard
        )

    except Exception as e:
        print(f"[ERROR] Saving idea failed: {e}")
        await message.answer(
            MESSAGES[language].get(
                'ERROR_SAVING_IDEA',
                "⚠️ Error saving the idea. Please try again later."
            )
        )
