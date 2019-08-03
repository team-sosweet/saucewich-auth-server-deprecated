from typing import Type, Dict, Any

from werkzeug.security import generate_password_hash

from app.models.connections import DBConnection


class Account:
    table_creation_query = """
        CREATE TABLE IF NOT EXISTS `account` (
            `seq` INT(11) AUTO_INCREMENT PRIMARY KEY,
            `username` VARCHAR(20) NOT NULL UNIQUE,
            `password` VARCHAR(100) NOT NULL
        );
    """

    connection: Type[DBConnection]

    async def initialize(cls, connection: Type[DBConnection]):
        cls.connection = connection
        await cls.connection.execute(cls.table_creation_query)

    @classmethod
    async def get(cls, username: str) -> Dict[str, str]:
        query = "SELECT * FROM `account` WHERE `username` = %s;"
        user =  await cls.connection.fetchone(
            query,
            username
        )
        return user

    @classmethod
    async def register(cls, username: str, password: str) -> bool:
        query = "INSERT INTO `account` VALUES (%s, %s)"
        try:
            await cls.connection.execute(
                query,
                (username, generate_password_hash(password))
            )
            return True
        except:
            return False
