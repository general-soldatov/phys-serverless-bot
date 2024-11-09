from dynamodb_fsm import FSMDynamodb
import time
import asyncio
# from handlers.question import Shedule
from app.connect.api_user import Shedule, UserApi
from app.connect.db_students import DBStudents, DatabaseConfig
from app.connect.db_user import DBUser
from datetime import datetime
import requests
import json
from app.config.config import TGbot
from handlers.users import BookSelector

async def all():
    result = FSMDynamodb().all_value()
    print(result)

def delete():
    data = ['fsm:980314213:980314213:aiogd:stack:', 'fsm:980314213:980314213:aiogd:context:oeMKX9', 'fsm:980314213:980314213:aiogd:context:lTGyx2', 'fsm:980314213:980314213:aiogd:context:F95JG6', 'fsm:980314213:980314213:aiogd:context:9vpGP4', 'fsm:980314213:980314213:aiogd:context:8P1sD9', 'fsm:980314213:980314213:aiogd:context:0eHBo4']
    for i in data:
        FSMDynamodb().delete_note(key=i)

def video_json():
    video_dict = {
        'mechanic': [
            ('Маятник Обербека', 'https://rutube.ru/video/0b103b6f1e448b787739f03e826115ce/'),
            ('Момент инерции кольца', 'https://rutube.ru/video/91f96617bdcd7392e8a38cd566743e32/'),
            ("Затухающие колебания сферического тела", "https://rutube.ru/video/cd7b1aebd2f3f3a643611b816d3c6083/"),
            ("Резонанс механических колебаний", "https://rutube.ru/video/0851ca770c1e888f8d1c30243dbbe2e3/"),
            ("Инерция физического маятника", "https://rutube.ru/video/283c140cec8c9cc32049374f21140432/"),
            ("Маятник Максвелла", "https://rutube.ru/video/28ce8a8263e35e49e1046d06aaca2ce5/"),
            ("Виды соударений", "https://rutube.ru/video/2d50b2b1bbdecf01cf3ca1f27bee2354/"),
            ("Инерция диска", "https://rutube.ru/video/87ea3ee38a0e669ec6440b5f8852028e/"),
        ],
        'mkt': [
            ("Адиабатный процесс", "https://rutube.ru/video/98c182b2114d251c9ea474698b2952b5/"),
            ("Динамическая вязкость", "https://rutube.ru/video/936599c107bcc22fc2c80ad807866bf3/"),
        ],
        'electrical': [
            ("Магнитная индукция поля Земли", "https://rutube.ru/video/36a14f8957059fbfc1ecca2078354553/"),
            ("Резонанс ЭМ-колебаний", "https://rutube.ru/video/79e1ea88d7542a91080bfc2173332fa4/"),
            ("Элетроёмкость конденсаторов", "https://rutube.ru/video/ea17a175e7f9f26f34a3ee13fb1845d5/"),
            ("Правила Кирхгофа", "https://rutube.ru/video/7a7a759ce21ec70401cd4948bff9fe8c/"),
            ("Мостик Уитстона", "https://rutube.ru/video/c6e8ff106a044833011f65530b4da790/"),
            ("Электростатический осциллограф", "https://rutube.ru/video/590def6479da4b37ecb6bf5be32748dd/"),
        ],
        'optics': [
            ("Закон Малюса", "https://rutube.ru/video/a44ca51ee0882dec540d33581f1a4f54/"),
            ("Дифракционная решётка", "https://rutube.ru/video/0636fd4b5eecea663ee992efddf5a51b/"),
        ]
    }
    with open('app/config/video.json', 'w', encoding='utf-8') as file:
        json.dump(video_dict, file, ensure_ascii=False, indent=4)

from typing import Optional

def req_video(category: Optional[str] = None):
    url = 'https://storage.yandexcloud.net/phys-bot/json/video.json'
    response = requests.get(url)
    data: dict = response.json()
    return data[category] if category else data

def database():
    db = DBStudents()
    # db = DatabaseConfig().__dict__
    print(db.score_user(profile='НТТС', group='9-а'))

def create_tables():
    """Функция для создания таблиц в БД
    """
    DBStudents().create_table()
    time.sleep(1)
    DBUser().create_table()

# DBUser().update_active(user_id=int(TGbot.admin), active=2)
# print(DBUser().info_user(int(TGbot.admin)))
# print(DBStudents().get_user(int(TGbot.admin)))

# create_tables()

def success_register(user_id = 1130164675, name = 'Плацында Алина Вячеслововна'):
    response = requests.get('https://storage.yandexcloud.net/phys-bot/json/contingent.json')
    data = response.json()[name]
    DBUser().update_active(user_id, active=2)
    DBStudents().register_student(user_id=user_id, name=name, **data)

print(DBStudents().get_user(1130164675))