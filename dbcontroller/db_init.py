from dbcontroller.db_objects_factory import DbObjectsFactory
from dbcontroller.models import TgPretension, \
    Manager, UserAccount, Order, TgUserAccount, TgManager
from datetime import datetime


if __name__ == "__main__":
    db_objects_factory = DbObjectsFactory()
    db_objects_factory.init()
    Manager.create(mail='biba', login='biba', password='1')
    Manager.create(mail='boba', login='boba', password='1')
    Manager.create(mail='zetta', login='zetta', password='1')

    UserAccount.create(mail='alfa', password='1', contract_number=1111)
    UserAccount.create(mail='beta', password='1', contract_number=1112)
    UserAccount.create(mail='gamma', password='1', contract_number=1113)

    Order.create(name="Лиотон 1000 Гель", info="Прямой антикоагулянт для наружного применения. При наружном применении оказывает местное антитромботическое, антиэкссудативное, умеренное противовоспалительное действие. Блокирует образование тромбина, угнетает активность гиалуронидазы, активирует фибринолитические свойства крови. Проникающий через кожу гепарин уменьшает воспалительный процесс и оказывает антитромботическое действие, улучшает микроциркуляцию и активирует тканевой обмен, благодаря этому ускоряет процессы рассасывания гематом и тромбов и уменьшения отечности тканей.", user_id = 1)
    Order.create(name="Беспроводной пылесос Tefal X-Force Flex 9.60 Allergy TY2039WO", info="Мощный и сверхлёгкий Tefal X-Force Flex 9.60 перевернёт ваши представления об эффективной, быстрой и комфортной уборке. Благодаря высокой мощности всасывания пылесос устраняет самые стойкие загрязнения без перерыва на подзарядку в течение 45 минут, а уникальная система Flex гарантирует безупречный порядок под низкой мебелью и в труднодоступных местах.", user_id=1)
    Order.create(name="Таблетки для посудомоечной машины Fairy Platinum All in One", info="Экологичные капсулы Fairy Platinum All in One с лимоном обеспечивают защиту компонентов посудомоечной машины и удаляют сложные загрязнения с посуды с первого раза, сообщая посуде приятный цитрусовый аромат, а посудомойке — чистоту и свежесть.", user_id=2)

    TgPretension.create(user_id=1, status='sended', _type=1, message='1', creation_datetime=datetime.now())
    TgPretension.create(user_id=1, status='processing', _type=2, message='2', creation_datetime=datetime.now())
    TgPretension.create(user_id=2, status='closed', _type=3, message='3', creation_datetime=datetime.now())
    TgPretension.create(user_id=3, status='closed', _type=4, message='4', creation_datetime=datetime.now())

    TgManager.create(tg_id=1, tg_username='cxfs', password='qwe', manager_id=1)
    TgManager.create(tg_id=2, tg_username='rxs', password='qwe', manager_id=2)
    TgManager.create(tg_id=3, tg_username='sxr', password='qwe', manager_id=3)

    TgUserAccount.create(tg_id=300438464, tg_username='24de', password='qwe', user_id=2, manager_id=2)
    TgUserAccount.create(tg_id=503521890, tg_username='drvfd', password='qwe', user_id=1, manager_id=1)