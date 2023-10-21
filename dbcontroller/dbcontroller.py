from peewee import (
    SqliteDatabase, Model, CharField, IntegerField,
    ForeignKeyField, DateTimeField
)

from get_config import get_config


config = get_config()
db = SqliteDatabase(config['db_file'])


class DataBaseController:
    def __init__(self, _db):
        self._db = _db

    def __enter__(self):
        self._db.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.close()

    def init(self):
        self._db.create_tables([UserAccount, TgUserAccount,
                               Order, Manager, Pretension])

    @staticmethod
    def create(model: type(Model), **kwargs) -> Model:
        instance = model(**kwargs)
        instance.save()
        return instance

    @staticmethod
    def get_user_ids() -> list:
        users = TgUserAccount.select()
        return [user.tg_id for user in users]

    @staticmethod
    def get_manager_ids() -> list:
        users = TgUserAccount.select()
        return [user.tg_id for user in users]

    def create_accounts_link(self):
        return

    def get_user_accounts_creds(self):
        return


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


if __name__ == '__main__':
    with DataBaseController(db) as controller:
        order = controller.create(Order, name='name', info='info')
        manager = controller.create(Manager, tg_id=1, tg_username='name',
                                    password='pass')
        user = controller.create(UserAccount, mail='mail', password='pass',
                                 contract_number=1, order_id=order.id)
        controller.create(TgUserAccount, tg_id=1, tg_username='name',
                          account_id=user.id, manager_id=manager.id)
        controller.init()
        user_ids = controller.get_user_ids()
        print(user_ids)
        manager_ids = controller.get_manager_ids()
        print(manager_ids)
