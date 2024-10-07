from dataclasses import dataclass
from os import getenv
import toml

# Загрузка TOML-файла
data = toml.load('app/config/data.toml')

@dataclass
class TGbot:
    token: str = getenv('TOKEN')
    admin: str = '980314213'
    shedule: str = getenv('API_SHEDULE')

@dataclass
class StudyConfig:
    weekday = data['study']['weekday']
    select_day = list(data['study']['select_day'])