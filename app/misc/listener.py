from sanic import Sanic

from app.models.account import Account
from app.models.connections import RedisConnection, MySQLConnection
from app.models.session import Session


async def initialize_connections(app, loop):
    await MySQLConnection.initialize({
        'use_unicode': True,
        'charset': 'utf8mb4',
        'user': 'root',
        'password': '',
        'db': 'saucewich',
        'host': 'localhost',
        'port': 3306,
        'loop': None,
        'autocommit': True,
    })

    await RedisConnection.initialize({
        'address': 'redis://localhost'
    })


async def initialize_models(app, loop):
    await Account.initialize(MySQLConnection)
    Session.initialize(RedisConnection)


async def destroy_connections(app, loop):
    await MySQLConnection.destroy()
    await RedisConnection.destroy()


def register_listeners(app: Sanic):
    app.register_listener(initialize_connections, 'before_server_start')
    app.register_listener(initialize_models, 'before_server_start')
    app.register_listener(initialize_models, 'before_server_stop')
