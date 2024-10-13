from dataclasses import dataclass, field
from os import getenv
import toml
from typing import Dict, Any

# Загрузка TOML-файла
data = toml.load('app/config/data.toml')
lexicon = toml.load('app/config/lexicon.toml')

@dataclass
class TGbot:
    token: str = getenv('TOKEN')
    admin: str = '980314213'
    shedule: str = getenv('API_SHEDULE')

@dataclass
class StudyConfig:
    weekday = data['study']['weekday']
    select_day = list(data['study']['select_day'])

BUTTONS_RU = lexicon['buttons_ru']
ADMIN = lexicon['admin']
USER = lexicon['user']
# COMMANDS = data['commands']