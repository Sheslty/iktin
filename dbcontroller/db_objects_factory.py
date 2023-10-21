from dbcontroller.models import (
    Order, Manager, TgUserAccount, UserAccount, TgPretension, TgManager
)


class DbObjectsFactory:
    order = Order
    manager = Manager
    tg_manager = TgManager
    tg_user_account = TgUserAccount
    user_account = UserAccount
    tg_pretension = TgPretension

    def init(self):
        self.order.create_table(safe=True)
        self.manager.create_table(safe=True)
        self.tg_user_account.create_table(safe=True)
        self.user_account.create_table(safe=True)
        self.tg_manager.create_table(safe=True)
        self.tg_pretension.create_table(safe=True)

    def create_order(self, **kwargs) -> Order:
        return self.order.create(**kwargs)

    def create_manager(self, **kwargs) -> Manager:
        return self.manager.create(**kwargs)

    def create_tg_user_account(self, **kwargs) -> TgUserAccount:
        return self.tg_user_account.create(**kwargs)

    def create_user_account(self, **kwargs) -> UserAccount:
        return self.user_account.create(**kwargs)

    def create_pretension(self, **kwargs) -> TgPretension:
        return self.pretension.create(**kwargs)


if __name__ == '__main__':
    c = DbObjectsFactory()
    c.init()
    c.create_tg_user_account(tg_id=300438464, tg_username='qwe', password='qwe', account_id=2, manager_id=2)