from datetime import datetime
from pathlib import Path
from json import load

from peewee import (
    SqliteDatabase, Model, CharField, IntegerField,
    ForeignKeyField, DateTimeField, FloatField
)


def get_config() -> dict:
    with open(Path('dbcontroller', 'config.json')) as f:
        return load(f)


config = get_config()
db = SqliteDatabase(config['db_file'])


class Manager(Model):
    mail = CharField(null=False, unique=True)
    login = CharField(null=False, unique=True)
    password = CharField(null=False)

    class Meta:
        database = db
        db_table = 'managers'


class UserAccount(Model):
    mail = CharField(null=False, unique=True)
    password = CharField(null=False)
    contract_number = IntegerField(null=False, unique=True)

    class Meta:
        database = db
        db_table = 'user_accounts'


class Order(Model):
    name = CharField(null=False)
    info = CharField()
    user_id = ForeignKeyField(UserAccount, on_delete='CASCADE')
    longitude = FloatField(null=True)
    latitude = FloatField(null=True)

    class Meta:
        database = db
        db_table = 'orders'


class TgManager(Model):
    tg_id = IntegerField(null=False, unique=True)
    tg_username = CharField(null=False)
    manager_id = ForeignKeyField(Manager, on_delete='CASCADE')

    class Meta:
        database = db
        db_table = 'tg_managers'


class TgUserAccount(Model):
    tg_id = IntegerField(null=False, unique=True)
    tg_username = CharField(null=False)
    user_id = ForeignKeyField(UserAccount, on_delete='CASCADE')
    manager_id = ForeignKeyField(TgManager, on_delete='SET NULL', null=True)

    class Meta:
        database = db
        db_table = 'tg_user_accounts'


class TgPretension(Model):
    user_id = ForeignKeyField(TgUserAccount, null=False, on_delete='CASCADE')
    status = CharField(null=False)
    _type = CharField(null=False)
    message = CharField()
    creation_datetime = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        db_table = 'tg_pretensions'
