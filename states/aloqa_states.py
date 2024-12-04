from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

class BotStates(StatesGroup):
    reklama_state = State()
    name_state = State()
    contacter = State()
    reklame_video = State()
