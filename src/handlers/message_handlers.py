"""
File contains handlers for dialog with bot
"""
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from server import dp, bot
from messages import messages
import translator
from database import db
from FSM.states import LanguageChange, LanguageChoose


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point. Handles "start" command and
    sets state for language input
    """
    await bot.send_message(message.chat.id, messages["start_msg"])

    # Set state
    await LanguageChoose.language.set()

    await message.answer(messages["choose_lang_start"])


@dp.message_handler(state=LanguageChange.language, commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    This method is called when user uses command
    'cancel' during language change.
    Method clears state and sends message about it
    """
    current_state = await state.get_state()
    logging.info('Cancelling state %r', current_state)
    # Cancel state
    await state.finish()
    await message.answer(messages["cancel"])


@dp.message_handler(commands='help')
async def help_cmd(message: types.Message):
    """
    This method handles help command
    and sends info about bot and how to use it
    """
    await message.answer(messages["help_msg"])


@dp.message_handler(commands='lang')
async def change_language_handler(message: types.Message):
    """
    This method handles command 'lang' which is used to
    change user's language. Bot sends message for user to input
    language code and sets state for FSM
    """
    await LanguageChange.language.set()
    user_language = db.get_col("user", message.from_user.id, "lang")
    await bot.send_message(message.chat.id,
                           messages["change_lang"].format(user_language)
                           )


@dp.message_handler(state=LanguageChoose.language)
async def add_language(message: types.Message, state: FSMContext):
    """
    This method handles language choose after start command
    and adds language code to db
    """
    if message.text not in translator.get_languages():
        await message.reply(messages["choose_lang_unknown"])
        return
    if db.get_col("user", message.from_user.id, "telegram_id"):
        db.update("user", message.from_user.id, {"lang": message.text})
    else:
        db.insert("user", {"telegram_id": message.from_user.id, "lang": message.text})
    await message.answer(messages["choose_lang_success"])
    await message.answer(messages["start_instruction"])
    await state.finish()


@dp.message_handler(state=LanguageChange.language)
async def change_language(message: types.Message, state: FSMContext):
    """
    This method handles language code after 'lang' command and updates
    database
    """
    if message.text not in translator.get_languages():
        await message.reply(messages["change_lang_unknown"])
        return
    db.update("user", message.from_user.id, {"lang": message.text})
    await message.answer(messages["change_lang_success"])
    await state.finish()


@dp.message_handler()
async def translate(message: types.Message):
    """
    This method is called whenever user sends any text
    and translates it to chosen language
    """
    user_language = db.get_col("user", message.from_user.id, "lang")
    translation = translator.translate(message.text, user_language)
    await message.reply(
        messages["translated_msg"].format(
            lang_from=translation.src,
            lang_to=user_language,
            translation=translation.text
        )
    )
