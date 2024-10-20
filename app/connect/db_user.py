import boto3
import logging
from boto3.dynamodb.conditions import Key
from os import getenv
from dotenv import load_dotenv
from app.config.config import DatabaseConfig
from typing import Union

logger = logging.getLogger(__name__)

class DBUser:
    """Класс для управления записями в базе данных YDB, название класса не принципиально.
    """
    def __init__(self, config: Union[DatabaseConfig, dict] = DatabaseConfig(),
                 table_name: str = 'User_Unauthorized'):
        """Инициализация базы данных и сервисного аккаунта, в целях безопасности используются
           переменные окружения, либо указанные в файле .env
        """
        if isinstance(config, DatabaseConfig):
            db_config = config.__dict__
        else:
            db_config = config

        self.dynamodb = boto3.resource('dynamodb', **db_config)
        self.dynamodb_client = boto3.client('dynamodb', **db_config)
        self.table_name = table_name

    def create_table(self):
        """Метод создания таблицы, инициализируются ключи и столбцы таблицы
        """
        table = self.dynamodb.create_table(
            TableName = self.table_name,
            KeySchema = [
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'  # Ключ партицирования, можно добавить дополнительно ключ сортировки Range
                }
            ],
            AttributeDefinitions = [
                {
                "AttributeName": "user_id",
                "AttributeType": "N"
                },
                {
                "AttributeName": "name",
                "AttributeType": "S"
                },
                {
                "AttributeName": "active",
                "AttributeType": "N"
                }
            ]
        )
        return table

    def put_item(self, user_id: int, name: str, active=1):
        """Метод добавления записи в таблицу.
        """
        table = self.dynamodb.Table(self.table_name)
        response = table.put_item(
            Item = {
                    'user_id': user_id,
                    'name': name,
                    'active': active,
            }
        )
        return response

    def update_active(self, user_id: int, active: int):
        """Метод смены активности в случае блокировки бота пользователем.
        """
        table = self.dynamodb.Table(self.table_name)
        response = table.update_item(
            Key = {
                'user_id': user_id
            },
            UpdateExpression = "set active = :a ",
            ExpressionAttributeValues = {
                ':a': active
            },
            ReturnValues = "UPDATED_NEW"
        )
        return response

    def info_user(self, user_id: int):
        """Метод запроса информации по ключу партицирования
        """
        table = self.dynamodb.Table(self.table_name)
        response = table.query(
            ProjectionExpression = 'user_id, name, active',
            KeyConditionExpression = Key('user_id').eq(user_id)
        )
        return response['Items']

    def all_users(self):
        """Метод сканирования всех элементов таблицы.
        """
        table = self.dynamodb.Table(self.table_name)
        return table.scan()['Items']

    def for_mailer(self, active: list = [1, 2]):
        """Метод выгрузки ключей таблицы для рассылки
        """
        table = self.dynamodb.Table(self.table_name)
        scan_kwargs = {
            'ProjectionExpression': "user_id, active"
        }
        response = table.scan(**scan_kwargs)

        return [int(item['user_id']) for item in response['Items'] if int(item['active']) in active]

    def mailer_user(self, active=1):
        """Метод выгрузки ключей таблицы для рассылки
        """
        filter_expression = "active = :a"
        expression_attribute_values = {":a": {"a": f"{active}"}}

        try:
            response = self.dynamodb_client.scan(
                TableName=self.table_name,
                FilterExpression=filter_expression,
                ProjectionExpression='user_id',
                ExpressionAttributeValues=expression_attribute_values
            )
            return [int(item['user_id']['N']) for item in response['Items']]

        except Exception as e:
            logger.error(e)

    def delete_note(self, user_id):
        """Метод удаления записи из базы данных.
        """
        table = self.dynamodb.Table(self.table_name)
        try:
            response = table.delete_item(
                Key = {'user_id': user_id},
                )
            return response

        except Exception as e:
            print('Error', e)


    def delete_table(self):
        """Метод удаления таблицы из базы данных
        """
        table = self.dynamodb.Table(self.table_name)
        table.delete()