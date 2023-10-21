from pathlib import Path
from json import load

from peewee import (
    SqliteDatabase, Model, CharField, IntegerField,
    ForeignKeyField, DateTimeField
)


def get_config() -> dict:
    with open(Path('dbcontroller', 'config.json')) as f:
        return load(f)


config = get_config()
db = SqliteDatabase(config['db_file'])


class Order(Model):
    name = CharField()
    info = CharField()

    class Meta:
        database = db


class UserAccount(Model):
    mail = CharField(null=False, unique=True)
    password = CharField(null=False)
    contract_number = IntegerField(null=False, unique=True)
    order_id = ForeignKeyField(Order, on_delete='SET NULL')

    class Meta:
        database = db


class TgUserAccount(Model):
    tg_id = IntegerField(null=False, unique=True)
    tg_username = CharField(null=False)
    account_id = ForeignKeyField(UserAccount, on_delete='CASCADE')
    manager_id = ForeignKeyField(UserAccount, on_delete='SET NULL')

    class Meta:
        database = db


class Manager(Model):
    tg_id = IntegerField(null=False, unique=True)
    tg_username = CharField(null=False)
    password = CharField(null=False)

    class Meta:
        database = db


class Pretension(Model):
    user_id = ForeignKeyField(TgUserAccount, null=False, on_delete='CASCADE')
    status = CharField(null=False)
    _type = IntegerField(null=False)
    message = CharField()
    creation_datetime = DateTimeField()

    class Meta:
        database = db
