"""
This file contains classes for FSM
"""

from aiogram.dispatcher.filters.state import State, StatesGroup


class LanguageChange(StatesGroup):
    language = State()


class LanguageChoose(StatesGroup):
    language = State()
