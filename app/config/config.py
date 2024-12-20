import boto3
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


@dataclass
class StudyConfig:
    weekday = data['study']['weekday']
    select_day = list(data['study']['select_day'])
    tasks = data['study']['tasks']
    contact = data['contact']
    metodic = data['metodic']
    books = data['books']

@dataclass
class AdminConfig:
    mailer = data['mailer']
    profile = data['mailer']['profile']

@dataclass
class DatabaseConfig:
    endpoint_url: str = getenv('ENDPOINT')
    region_name: str = getenv('REGION_NAME')
    aws_access_key_id: str = getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key: str = getenv('AWS_SECRET_ACCESS_KEY')


BUTTON = lexicon['buttons_ru']
ADMIN = lexicon['admin']
USER = lexicon['user']
COMMANDS = lexicon['commands']
