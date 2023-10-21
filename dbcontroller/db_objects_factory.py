from dbcontroller.models import (
    Order, Manager, TgUserAccount, UserAccount, Pretension
)


class DbObjectsFactory:
    order = Order
    manager = Manager
    tg_user_account = TgUserAccount
    user_account = UserAccount
    pretension = Pretension

    def init(self):
        self.order.create_table()
        self.manager.create_table()
        self.tg_user_account.create_table()
        self.user_account.create_table()
        self.pretension.create_table()

    def create_order(self, **kwargs) -> Order:
        return self.order.create(**kwargs)

    def create_manager(self, **kwargs) -> Manager:
        return self.manager.create(**kwargs)

    def create_tg_user_account(self, **kwargs) -> TgUserAccount:
        return self.tg_user_account.create(**kwargs)

    def create_user_account(self, **kwargs) -> UserAccount:
        return self.user_account.create(**kwargs)

    def create_pretension(self, **kwargs) -> Pretension:
        return self.pretension.create(**kwargs)
