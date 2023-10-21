from pathlib import Path
from json import load

from peewee import (
    SqliteDatabase, Model, CharField, IntegerField,
    ForeignKeyField, DateTimeField, PrimaryKeyField
)


def get_config() -> dict:
    with open(Path('dbcontroller', 'config.json')) as f:
        return load(f)


config = get_config()
db = SqliteDatabase(config['db_file'])

class Managers(Model):
    mail = CharField(null=False, unique=True)
    login = CharField(null=False, unique=True)
    password = CharField(null=False)

    class Meta:
        database = db
        db_table = 'managers'


class UserAccounts(Model):
    mail = CharField(null=False, unique=True)
    password = CharField(null=False)
    contract_number = IntegerField(null=False, unique=True)

    class Meta:
        database = db
        db_table = 'user_accounts'

class Orders(Model):
    name = CharField(null=False)
    info = CharField()
    account_id = ForeignKeyField(UserAccounts, on_delete='CASCADE')
    class Meta:
        database = db
        db_table = 'orders'

class TgUserAccounts(Model):
    tg_id = IntegerField(null=False, unique=True)
    tg_username = CharField(null=False)
    account_id = ForeignKeyField(UserAccounts, on_delete='CASCADE')
    manager_id = ForeignKeyField(UserAccounts, on_delete='SET NULL', null=True)

    class Meta:
        database = db
        db_table = 'tg_user_accounts'


class TgManagers(Model):
    tg_id = IntegerField(null=False, unique=True)
    tg_username = CharField(null=False)
    password = CharField(null=False)
    account_id = ForeignKeyField(Managers, on_delete='CASCADE')
    class Meta:
        database = db
        db_table = 'tg_manager'


class TgPretensions(Model):
    user_id = ForeignKeyField(TgUserAccounts, null=False, on_delete='CASCADE')
    status = CharField(null=False)
    _type = IntegerField(null=False)
    message = CharField()
    creation_datetime = DateTimeField()

    class Meta:
        database = db
        db_table = 'tg_pretension'
