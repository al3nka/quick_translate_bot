"""
File with methods to translate text using googletrans library
"""
from googletrans import Translator, LANGUAGES, Translated

translator = Translator()


def translate(text: str, language: str) -> Translated:
    """
    This method is used to translate text
    :param text: Text to translate
    :param language: language into which to translate
    :return: Translated object with info about translation
    """
    translation = translator.translate(text, dest=language)
    return translation


def get_languages() -> dict[str, str]:
    """
    This method is used to get all the languages available
    for translation with googletrans
    :return: dict of languages
    """
    return LANGUAGES
