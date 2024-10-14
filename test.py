from dynamodb_fsm import FSMDynamodb
import asyncio
# from handlers.question import Shedule
from app.api.user_api import Shedule
from datetime import datetime
import requests
import json

async def all():
    result = FSMDynamodb().all_value()
    print(result)

def delete():
    data = ['fsm:980314213:980314213:aiogd:stack:', 'fsm:980314213:980314213:aiogd:context:oeMKX9', 'fsm:980314213:980314213:aiogd:context:lTGyx2', 'fsm:980314213:980314213:aiogd:context:F95JG6', 'fsm:980314213:980314213:aiogd:context:9vpGP4', 'fsm:980314213:980314213:aiogd:context:8P1sD9', 'fsm:980314213:980314213:aiogd:context:0eHBo4']
    for i in data:
        FSMDynamodb().delete_note(key=i)

def books():
    book_dict = {
        'metodic' : {
            'mechanic_mkt': 'https://drive.google.com/file/d/10ToIHwEVfMOCmsB3Rx0MrTMO3HguWWcF/view?usp=sharing',
            'electrical': 'https://drive.google.com/file/d/10IN4eIFwDeObEX-VOdgGNwriSuC1d9rj/view?usp=sharing',
            'optics': 'https://drive.google.com/file/d/10PhhtqlFOLd8hOn8vFnjAt5ejQDGqcMG/view?usp=sharing'
        },
        'textbook': {
            'physics': 'https://drive.google.com/file/d/1-vqc9NgTDGwn_ZLUX4hrDg4qnqAtoFsc/view?usp=sharing'
        }
    }
    with open('app/config/books.json', 'w', encoding='utf-8') as file:
        json.dump(book_dict, file, ensure_ascii=False, indent=4)

from typing import Optional

def req_book(book: Optional[str] = None):
    url = 'https://storage.yandexcloud.net/phys-bot/json/books.json'
    response = requests.get(url)
    data: dict = response.json()
    return data[book] if book else data
