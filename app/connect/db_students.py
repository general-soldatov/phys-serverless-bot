import boto3
import logging

from app.config.config import DatabaseConfig
from typing import Union

logger = logging.getLogger(__name__)

class DBStudents:
    def __init__(self, config: Union[DatabaseConfig, dict] = DatabaseConfig(),
                 table_name: str = 'User_Var'):
        if isinstance(config, DatabaseConfig):
            db_config = config.__dict__
        else:
            db_config = config

        self.dynamodb = boto3.resource('dynamodb', **db_config)
        self.dynamodb_client = boto3.client('dynamodb', **db_config)
        self.table_name = table_name

    def create_table(self):
        table = self.dynamodb.create_table(
            TableName = self.table_name,
            KeySchema = [
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'  # Ключ партицирования
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
                "AttributeName": "profile",
                "AttributeType": "S"
                },
                {
                "AttributeName": "group",
                "AttributeType": "S"
                },
                {
                "AttributeName": "fine",
                "AttributeType": "N"
                },
                {
                "AttributeName": "prize",
                "AttributeType": "N"
                }

            ]
        )
        return table

    def register_student(self, user_id, name, profile, group, fine=0, prize=0, google_id=0):
        table = self.dynamodb.Table(self.table_name)
        tasks = {'S0': 0}
        bonus = {
            'static': 0,
            'kinematic': 0,
            'dynamic': 0
        }
        response = table.put_item(
            Item = {
                    'user_id': user_id,
                    'name': name,
                    'profile': profile,
                    'group': group,
                    'fine': fine,
                    'prize': prize,
                    'tasks': tasks,
                    'bonus': bonus
            }
        )
        return response

    def add_task(self, user_id, task, ball):
        table = self.dynamodb.Table(self.table_name)
        response = table.update_item(
            Key = {
                'user_id': user_id
            },
            UpdateExpression = f"set tasks.{task} = :t ",
            ExpressionAttributeValues = {
                ':t': ball
            },
            ReturnValues = "UPDATED_NEW"
        )
        return response

    def set_fine(self, user_id, fine):
        table = self.dynamodb.Table(self.table_name)
        response = table.update_item(
            Key = {
                'user_id': user_id
            },
            UpdateExpression = f"set fine = :f ",
            ExpressionAttributeValues = {
                ':f': fine
            },
            ReturnValues = "UPDATED_NEW"
        )
        return response

    def set_prize(self, user_id, prize):
        table = self.dynamodb.Table(self.table_name)
        response = table.update_item(
            Key = {
                'user_id': user_id
            },
            UpdateExpression = f"set prize = :p ",
            ExpressionAttributeValues = {
                ':p': prize
            },
            ReturnValues = "UPDATED_NEW"
        )
        return response

    def get_user(self, user_id):
        """Метод запроса информации о пользователе по ключу партицирования
        """
        table = self.dynamodb.Table(self.table_name)
        response = table.get_item(
            Key = {
                'user_id': user_id
            }
        )
        return response['Item']


    def add_bonus(self, user_id, category, task):
        table = self.dynamodb.Table(self.table_name)
        response = table.update_item(
            Key = {
                'user_id': user_id
            },
            UpdateExpression = f"set bonus.{category} = :b ",
            ExpressionAttributeValues = {
                ':b': task
            },
            ReturnValues = "UPDATED_NEW"
        )
        return response


    def all_users(self):
        table = self.dynamodb.Table(self.table_name)
        return table.scan()['Items']

    def score_user(self, profile: str, group: str):
        filter_expression = "profile = :p AND group = :g"
        expression_attribute_values = {
            ":p": {"S": f"{profile}"},
            ":g": {"S": f"{group}"},
            }

        try:
            response = self.dynamodb_client.scan(
                TableName=self.table_name,
                FilterExpression=filter_expression,
                ProjectionExpression='user_id, name, fine, prize',
                ExpressionAttributeValues=expression_attribute_values
            )
            return [{
                'user_id': int(item['user_id']['N']),
                'name': item['name']['S'],
                'fine': int(item['fine']['N']),
                'prize': int(item['prize']['N'])
                     }
                     for item in response['Items']]

        except Exception as e:
            logger.error(e)

    def mailer_user(self, profile, group=None):
        """Метод выгрузки ключей таблицы для рассылки
        """
        if not group:
            filter_expression = "profile = :p"
            expression_attribute_values = {":p": {"S": f"{profile}"}}
        else:
            filter_expression = "profile = :p AND group = :g"
            expression_attribute_values = {
                ":p": {"S": f"{profile}"},
                ":g": {"S": f"{group}"},
                }
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
        table = self.dynamodb.Table(self.table_name)
        try:
            response = table.delete_item(
                Key = {'user_id': user_id},
                )
            return response

        except Exception as e:
            print('Error', e)


    def delete_table(self):
        table = self.dynamodb.Table(self.table_name)
        table.delete()