"""
File contains inline mode handlers
"""
import hashlib
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle

from server import dp, bot
from messages import messages
import translator
from database import db


@dp.inline_handler()
async def inline_translate(inline_query: InlineQuery):
    """
    This method is used to make inline mode translate
    so the user can translate text in chat.
    Translator translates all the text that user writes
    and sends message with translation
    """
    text = inline_query.query
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    if not db.get_col("user", inline_query.from_user.id, "telegram_id"):
        return
    user_language = db.get_col("user", inline_query.from_user.id, "lang")
    translation = translator.translate(text, user_language)
    input_content = InputTextMessageContent(
        messages["inline_translated_msg"].format(
            lang_from=translation.src,
            lang_to=user_language,
            text=text,
            translation=translation.text
        )
    )

    item = InlineQueryResultArticle(
        id=result_id,
        title=f'Translate {text!r}',
        input_message_content=input_content
    )
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)
