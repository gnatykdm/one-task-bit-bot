from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons import get_idea_conf_keyboard, menu_reply_keyboard, idea_reply_keyboard
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

async def process_idea_delete(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    if not user_find or not user_find.get("id"):
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    language = await UserService.get_user_language(user_id) or "ENGLISH"
    ideas = await IdeaService.get_all_ideas_by_user_id(user_id)

    print(f"--[DEBUG] User {user_id} ideas: {ideas}")

    try:
        user_number = int(message.text.strip())
    except ValueError:
        await message.answer(MESSAGES[language]['NOT_VALID_IDEA_NUM'], reply_markup=idea_reply_keyboard())
        return

    index = user_number - 1
    if not (0 <= index < len(ideas)):
        await message.answer(MESSAGES[language]['INVALID_IDEA_NUM'], reply_markup=idea_reply_keyboard())
        return

    idea_to_delete = ideas[index]
    real_id = idea_to_delete["id"]

    print(f"--[DEBUG] Deleting idea with id {real_id} for user {user_id}")

    await IdeaService.delete_user_idea(real_id)

    await message.answer(MESSAGES[language]['IDEA_DELETED'].format(user_number, idea_to_delete['idea_name']), reply_markup=idea_reply_keyboard())
    await state.clear()