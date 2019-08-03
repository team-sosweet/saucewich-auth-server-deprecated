from typing import Type, Dict, Any

from app.repositories.connections import DBConnection


class AccountRepository:
    table_creation_query = """
        CREATE TABLE IF NOT EXISTS `account` (
            `seq` INT(11) AUTO_INCREMENT PRIMARY KEY,
            `username` VARCHAR(20) NOT NULL UNIQUE,
            `password` VARCHAR(100) NOT NULL
        );
    """

    def __init__(self, connection: Type[DBConnection]):
        self.connection = connection

    def get(self, username: str) -> Dict[str, str]:
        query = "SELECT * FROM `account` WHERE `username` = %s;"
        user =  self.connection.fetchone(
            query,
            username
        )
        return user
