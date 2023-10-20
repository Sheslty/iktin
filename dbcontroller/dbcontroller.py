import sqlite3
import logging

DEFAULT_DB_FILE = 'dbfile.db'


class DataBaseController:
    def __init__(self, db=DEFAULT_DB_FILE):
        self.conn = sqlite3.connect(db)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def __execute_cmd(self, cmd):
        try:
            logging.debug(f'Execute CMD: {cmd}')
            cursor = self.conn.cursor()
            cursor.execute(cmd)
            res = cursor.fetchall()
            if res is None:
                return []
            return res

        except Exception as ex:
            logging.error(f'Exception while executing cmd {cmd}: {ex}')
            raise

    def __execute_and_commit_cmd(self, cmd):
        try:
            self.__execute_cmd(cmd)
            self.conn.commit()
        except Exception as ex:
            logging.error(f'Exception while commit cmd {cmd}: {ex}')
            self.conn.rollback()
            raise

    def init(self):
        try:
            cmd = "CREATE TABLE IF NOT EXISTS user_accounts (" \
                  "     id INT PRIMARY KEY AUTOINCREMENT," \
                  "     mail TEXT NOT NULL UNIQUE," \
                  "     password TEXT NOT NULL," \
                  "     contract_number INT NOT NULL UNIQUE," \
                  "     order_id INT," \
                  ");"
            self.__execute_cmd(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS orders (" \
                  "     id INT PRIMARY KEY AUTOINCREMENT," \
                  "     name TEXT," \
                  "     info TEXT," \
                  ");"
            self.__execute_cmd(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS tg_users (" \
                  "     id INT PRIMARY KEY AUTOINCREMENT," \
                  "     tg_id INT UNIQUE," \
                  "     tg_username TEXT," \
                  "     account_id  INT," \
                  "     manager_id  INT" \
                  ");"
            self.__execute_cmd(cmd)
            cmd = "CREATE TABLE IF NOT EXISTS managers (" \
                  "     id INT PRIMARY KEY AUTOINCREMENT," \
                  "     tg_id INT UNIQUE," \
                  "     tg_username TEXT," \
                  "     password TEXT NOT NULL" \
                  ");"
            self.__execute_cmd(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS pretension (" \
                  "     id INT PRIMARY KEY AUTOINCREMENT," \
                  "     user_id INT UNIQUE," \
                  "     status TEXT," \
                  "     type INT," \
                  "     message INT," \
                  "     creation_datetime DATETIME" \
                  ");"
            self.__execute_cmd(cmd)

            self.conn.commit()

        except Exception as ex:
            logging.exception(f'Database init error {ex}')
            self.conn.rollback()
