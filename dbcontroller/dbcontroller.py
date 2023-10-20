import sqlite3
import logging

DEFAULT_DB_FILE = 'dolphin-subscribers.db'


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
            cmd = "CREATE TABLE IF NOT EXISTS subscribers (" \
                  "     id INTEGER PRIMARY KEY," \
                  "     tg_id INT NOT NULL UNIQUE," \
                  "     username CHAR NOT NULL," \
                  "     creation_datetime DATETIME," \
                  "     status INT NOT NULL," \
                  "     sub_days INT" \
                  ");"
            self.__execute_cmd(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS owners (" \
                  "     id INTEGER PRIMARY KEY," \
                  "     tg_id INT NOT NULL UNIQUE," \
                  "     username CHAR NOT NULL" \
                  ");"
            self.__execute_cmd(cmd)

            # TODO: sub_id
            # TODO: или понять что это за дракон https://surik00.gitbooks.io/aiogram-lessons/content/chapter4.html
            cmd = "CREATE TABLE IF NOT EXISTS transactions (" \
                  "     id INTEGER PRIMARY KEY," \
                  "     sub_id CHAR NOT NULL, " \
                  "     amount INT NOT NULL," \
                  "     status INT NOT NULL," \
                  "     date DATETIME" \
                  ");"
            self.__execute_cmd(cmd)

            self.conn.commit()

        except Exception as ex:
            logging.exception(f'Database init error {ex}')
            self.conn.rollback()
