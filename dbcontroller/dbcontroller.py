import sqlite3
import logging

from dbcontroller.sql_actions import SQlActions
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
                  "    id INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "    mail CHAR NOT NULL," \
                  "    password CHAR NOT NULL," \
                  "    contract_number INT NOT NULL," \
                  "    order_id INT," \
                  "    UNIQUE (contract_number, mail)," \
                  "    FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE SET NULL" \
                  ");"
            self.__execute_sql(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS orders (" \
                  "    id INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "    name CHAR," \
                  "    info CHAR" \
                  ");"
            self.__execute_sql(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS tg_users (" \
                  "    id INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "    tg_id INT NOT NULL UNIQUE," \
                  "    tg_username CHAR NOT NULL," \
                  "    account_id INT NOT NULL," \
                  "    manager_id INT NOT NULL," \
                  "    UNIQUE (tg_id)," \
                  "    FOREIGN KEY(account_id) REFERENCES user_accounts(id) ON DELETE CASCADE" \
                  "    FOREIGN KEY(manager_id) REFERENCES managers(id) ON DELETE SET NULL" \
                  ");"
            self.__execute_sql(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS managers (" \
                  "    id INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "    tg_id INT NOT NULL UNIQUE," \
                  "    tg_username CHAR NOT NULL," \
                  "    password CHAR NOT NULL" \
                  ");"
            self.__execute_sql(cmd)

            cmd = "CREATE TABLE IF NOT EXISTS pretension (" \
                  "    id INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "    user_id INT NOT NULL," \
                  "    status CHAR NOT NULL," \
                  "    type INT NOT NULL," \
                  "    message CHAR," \
                  "    creation_datetime DATETIME," \
                  "    FOREIGN KEY(user_id) REFERENCES tg_users(id) ON DELETE CASCADE" \
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

    def create_accounts_link(self):
        sql = SQlActions.GET_USER_ACCOUNTS_CREDS
        return self.__execute_sql(sql)

    def get_user_accounts_creds(self):
        sql = SQlActions.GET_USER_ACCOUNTS_CREDS
        return self.__execute_sql(sql)
