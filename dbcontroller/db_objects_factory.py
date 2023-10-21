from dbcontroller.models import (
    Orders, Managers, TgUserAccounts, UserAccounts, TgPretensions
)


class DbObjectsFactory:
    order = Orders
    manager = Managers
    tg_user_account = TgUserAccounts
    user_account = UserAccounts
    pretension = Pretensions

    def init(self):
        self.order.create_table()
        self.manager.create_table()
        self.tg_user_account.create_table()
        self.user_account.create_table()
        self.pretension.create_table()

    def create_order(self, **kwargs) -> Orders:
        return self.order.create(**kwargs)

    def create_manager(self, **kwargs) -> Managers:
        return self.manager.create(**kwargs)

    def create_tg_user_account(self, **kwargs) -> TgUserAccounts:
        return self.tg_user_account.create(**kwargs)

    def create_user_account(self, **kwargs) -> UserAccounts:
        return self.user_account.create(**kwargs)

    def create_pretension(self, **kwargs) -> TgPretensions:
        return self.pretension.create(**kwargs)
