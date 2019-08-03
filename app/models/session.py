import time
from datetime import datetime, time
from typing import Type

from app.models.connections import KVConnection


class Session:
    namespace = 'session'
    connection: Type[KVConnection]

    TTL = 1800

    def initialize(cls, connection: Type[KVConnection]):
        cls.connection = connection

    @classmethod
    async def add(cls, username: str, session_id: str):
        username_key = cls._make_key_with_namespace(username)
        session_id_key = cls._make_key_with_namespace(session_id)

        await cls.connection.set(username_key, {
            'session_id': session_id
        })
        await cls.connection.set(session_id_key, {
            'username': username,
            'created_at': time.time()
        })

        await cls.connection.expire(username_key, cls.TTL)
        await cls.connection.expire(session_id_key, cls.TTL)

    @classmethod
    async def remove(cls, *, username: str = None, session_id: str = None):
        if session_id is not None:
            session_id_key = cls._make_key_with_namespace(session_id)
            session_data = await cls.connection.get(session_id_key)

            username = session_data['username']
            username_key = cls._make_key_with_namespace(username)
        elif username is not None:
            username_key = cls._make_key_with_namespace(username)
            user_data = await cls.connection.get(username_key)

            session_id = user_data['session_id']
            session_id_key = await cls._make_key_with_namespace(session_id)
        else:
            raise TypeError('Either username and session_id need not be None.')

        cls.connection.delete(username_key)
        cls.connection.delete(session_id_key)

    @classmethod
    async def exists(cls, *, username: str = None, session_id: str = None):
        if session_id is not None:
            key = cls._make_key_with_namespace(session_id)
        elif username is not None:
            key = cls._make_key_with_namespace(username)
        else:
            raise TypeError('Either username and session_id need not be None.')

        return await cls.connection.exists(key)

    @classmethod
    def _make_key_with_namespace(cls, key) -> str:
        return f'{cls.namespace}:{key}'
