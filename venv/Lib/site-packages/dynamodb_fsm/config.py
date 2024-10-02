import boto3
from dataclasses import dataclass
from os import getenv
from dotenv import load_dotenv

@dataclass
class DatabaseConfig:
    endpoint_url: str = getenv('ENDPOINT')
    region_name: str = getenv('REGION_NAME')
    aws_access_key_id: str = getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key: str = getenv('AWS_SECRET_ACCESS_KEY')


load_dotenv()
config = DatabaseConfig().__dict__
