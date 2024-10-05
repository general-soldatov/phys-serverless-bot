import logging
import boto3
from boto3.dynamodb.conditions import Key

from aiogram.fsm.storage.base import BaseStorage, StorageKey, DefaultKeyBuilder
from aiogram.fsm.state import State
from typing import Any, Dict, Optional

from .config import config

logger = logging.getLogger(__name__)

class FSMDynamodb(BaseStorage):
    """ FSM on DynamoDB.
    This class stores information about user states in the FSM dialog.
    """

    def __init__(self, config=config, table_name: str = "fsm_storage_", with_destiny=False) -> None:
        # Dynamodatabase
        self.dynamodb = boto3.resource('dynamodb', **config)
        self.db_client = boto3.client('dynamodb', **config)
        self.table_name = table_name
        self.build = DefaultKeyBuilder(with_destiny=with_destiny)

    async def close(self) -> None:
        pass

    async def set_state(self, key: StorageKey, state = None) -> None:
        s_key = self.build.build(key)
        s_state = state.state if isinstance(state, State) else state
        table = self.dynamodb.Table(self.table_name)

        try:
            table.update_item(
                Key = {
                    'key': s_key
                },
                UpdateExpression = "set state = :s ",
                ExpressionAttributeValues = {
                    ':d': s_state
                },
                ReturnValues = "UPDATED_NEW")


        except Exception as e:
            logger.error(f"FSM Storage set_state error: {e}")


    async def get_state(self, key: StorageKey) -> Optional[str]:
        """
        Get key state

        :param key: storage key
        :return: current state
        """
        try:
            s_key = self.build.build(key)
            table = self.dynamodb.Table(self.table_name)
            response = table.get_item(
                Key = {
                    'key': s_key
                }
            )
            if 'Item' in response:
                return response['Item'].get('state', None)

        except self.db_client.exceptions.ResourceNotFoundException:
            self._create_table()
            return None

        except BaseException as e:
            logger.error(f"FSM Storage error get_state: {e}")

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        s_key = self.build.build(key)
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

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        """
        Get current data for key

        :param key: storage key
        :return: current data
        """
        s_key = self.build.build(key)
        table = self.dynamodb.Table(self.table_name)
        try:
            response = table.query(
                ProjectionExpression = 'data',
                KeyConditionExpression = Key('key').eq(s_key)
            )
            return response['Items'][0]['data'].copy() if response['Items'] else dict()

        except Exception as e:
            logger.error(f"FSM Storage error get_data: {e}")
            return None

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
                },
                {
                    "AttributeName": "state",
                    "AttributeType": "S"
                }
            ]
        )
        logger.error(f"FSM table is created with dynamodb.")

    def all_value(self):
        """
        Scan table`s values with dynamodatabase
        """
        table = self.dynamodb.Table(self.table_name)
        return table.scan()['Items']

    def delete_note(self, key):
        """
        Delete note with dynamodb
        """
        table = self.dynamodb.Table(self.table_name)
        try:
            response = table.delete_item(
                Key = {'key': key},
                )
            return response

        except Exception as e:
            print('Error', e)
