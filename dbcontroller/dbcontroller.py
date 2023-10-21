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

    def __execute_sql(self, cmd):
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

    def __execute_and_commit_sql(self, cmd):
        try:
            self.__execute_sql(cmd)
            self.conn.commit()
        except Exception as ex:
            logging.error(f'Exception while commit cmd {cmd}: {ex}')
            self.conn.rollback()
            raise

    def init(self):
        try:
            cmd = "CREATE TABLE IF NOT EXISTS user_accounts (" \
                  "     id INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "     mail CHAR NOT NULL," \
                  "     password CHAR NOT NULL," \
                  "     contract_number INT NOT NULL," \
                  "     order_id INT," \
                  "     UNIQUE (contract_number, mail)" \
                  ");"
            self.__execute_sql(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS orders (" \
                  "     id INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "     name CHAR," \
                  "     info CHAR" \
                  ");"
            self.__execute_sql(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS tg_users (" \
                  "     id INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "     tg_id INT NOT NULL," \
                  "     tg_username CHAR," \
                  "     account_id INT," \
                  "     manager_id INT" \
                  "     UNIQUE (tg_id)" \
                  ");"
            self.__execute_sql(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS managers (" \
                  "     id INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "     tg_id INT UNIQUE," \
                  "     tg_username CHAR," \
                  "     password CHAR NOT NULL" \
                  ");"
            self.__execute_sql(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS pretension (" \
                  "     id INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "     user_id INT UNIQUE," \
                  "     status CHAR," \
                  "     type INT," \
                  "     message INT," \
                  "     creation_datetime DATETIME" \
                  ");"
            self.__execute_sql(cmd)

            self.conn.commit()

        except Exception as ex:
            logging.exception(f'Database init error {ex}')
            self.conn.rollback()

    def get_users_ids(self):
        return ()

    def get_managers_ids(self):
        return ()
