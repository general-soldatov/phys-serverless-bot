import logging

import boto3
from boto3.dynamodb.conditions import Key

from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.fsm.state import State
from typing import Any, Dict, Optional

from .config import config

logger = logging.getLogger(__name__)

class FSMDynamodb(BaseStorage):
    """ FSM on DynamoDB.
    This class stores information about user states in the FSM dialog.
    """

    def __init__(self, config=config, table_name: str = "fsm_storage") -> None:
        # Dynamodatabase
        self.dynamodb = boto3.resource('dynamodb', **config)
        self.db_client = boto3.client('dynamodb', **config)
        self.table_name = table_name

    def _create_table(self) -> None:
        """
        Create table if not exists
        """
        self.dynamodb.create_table(
            TableName = self.table_name,
            KeySchema = [
                {
                    'AttributeName': 'key',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions = [
                {
                "AttributeName": "key",
                "AttributeType": "S"
                }
            ]
        )

    @staticmethod
    def _key(key: StorageKey) -> str:
        """
        Create a key for every uniqe user, chat and bot
        """
        return f'{key.bot_id}:{key.chat_id}:{key.user_id}'


    async def set_state(self, key: StorageKey, state: State | None = None) -> None:
        """
        Set state for specified key

        :param key: storage key
        :param state: new state
        """
        s_key = self._key(key)
        table = self.dynamodb.Table(self.table_name)

        try:
            table.update_item(
                Key = {
                    'key': s_key
                },
                UpdateExpression = "set state = :s ",
                ExpressionAttributeValues = {
                    ':s': state
                },
                ReturnValues = "UPDATED_NEW"
            )
        except Exception as e:
            logger.error(f"FSM Storage set_state error: {e}")

    async def get_state(self, key: StorageKey) -> Optional[str]:
        """
        Get key state

        :param key: storage key
        :return: current state
        """
        def _get_state():
            s_key = self._key(key)
            table = self.dynamodb.Table(self.table_name)
            response = table.get_item(
                Key = {
                    'key': s_key
                }
            )
            if 'Item' in response:
                return response['Item'].get('state', None)

        try:
            response = _get_state()
            return response

        except self.db_client.exceptions.ResourceNotFoundException:
            self._create_table()
            return _get_state()

        except BaseException as e:
            logger.error(f"FSM Storage error get_state: {e}")

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        """
        Write data (replace)

        :param key: storage key
        :param data: new data
        """
        s_key = self._key(key)
        table = self.dynamodb.Table(self.table_name)

        try:
            table.update_item(
                Key = {
                    'key': s_key
                },
                UpdateExpression = "set data = :d ",
                ExpressionAttributeValues = {
                    ':d': data
                },
                ReturnValues = "UPDATED_NEW")


        except Exception as e:
            logger.error(f"FSM Storage set_data error: {e}")

    async def get_data(self, key: StorageKey) -> Optional[Dict[str, Any]]:
        """
        Get current data for key

        :param key: storage key
        :return: current data
        """
        s_key = self._key(key)
        table = self.dynamodb.Table(self.table_name)

        try:
            response = table.query(
                ProjectionExpression = 'data',
                KeyConditionExpression = Key('key').eq(s_key)
            )

            return response['Items'][0]['data'] if response['Items'] else None

        except Exception as e:
            logger.error(f"FSM Storage error get_data: {e}")
            return None

    async def update_data(
        self, key: StorageKey, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update date in the storage for key (like dict.update)

        :param key: storage key
        :param data: partial data
        :return: new data
        """
        self.set_data(key, data)

    async def close(self) -> None:
        """
        Close storage (database connection, file or etc.)
        """
        pass
