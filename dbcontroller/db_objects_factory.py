from dbcontroller.models import (
    Orders, Managers, TgUserAccounts, UserAccounts, TgPretensions, TgManagers
)


class DbObjectsFactory:
    orders = Orders
    managers = Managers
    tg_user_accounts = TgUserAccounts
    user_accounts = UserAccounts
    tg_pretensions = TgPretensions
    tg_managers = TgManagers

    def init(self):
        self.orders.create_table()
        self.managers.create_table()
        self.tg_user_accounts.create_table()
        self.user_accounts.create_table()
        self.tg_pretensions.create_table()
        self.tg_managers.create_table()

    def create_order(self, **kwargs) -> Orders:
        return self.orders.create(**kwargs)

    def create_manager(self, **kwargs) -> Managers:
        return self.managers.create(**kwargs)

    def create_tg_manager(self, **kwargs) -> TgManagers:
        return self.tg_managers.create(**kwargs)

    def create_tg_user_account(self, **kwargs) -> TgUserAccounts:
        return self.tg_user_accounts.create(**kwargs)

    def create_user_account(self, **kwargs) -> UserAccounts:
        return self.user_accounts.create(**kwargs)

    def create_tg_pretension(self, **kwargs) -> TgPretensions:
        return self.tg_pretensions.create(**kwargs)


if __name__ == '__main__':
    c = DbObjectsFactory()
    c.create_manager(tg_id=10, tg_username='qwe', password='qwe')