# -*- coding: utf-8 -*-

# python-ldap library test
import ldap
from ldap import sasl
from pprint import pprint
from utils import ldapom

#LDAP_HOST = '195.189.111.9'
#LDAP_PORT = 4389

LDAP_HOST = '10.100.1.66'
LDAP_PORT = 389

LDAP_USERNAME = 'uid=zimbra,cn=admins,cn=zimbra'
LDAP_PASSWORD = 'q_DXNyB0Ym'

server = 'ldap://%s:%d' % (LDAP_HOST, LDAP_PORT)



lc = ldapom.LdapConnection(uri=server, base='dc=chukreev,dc=com',
                           login=LDAP_USERNAME, password=LDAP_PASSWORD)

# 1. Вы вести список доменов
domain_list = lc.query(filter="(zimbraDomainName=*)", retrieve_attributes=None, base='', scope=ldap.SCOPE_SUBTREE)
"""
Этот результат будет фильтроваться с помощью mysql таблички прав, заполняемой через django.contrib.admin
"""

# 2. Способы аутентификации
domain_outer_auth_list = lc.query(filter="(zimbraAuthMech=ad)", retrieve_attributes=None, base='', scope=ldap.SCOPE_SUBTREE)
domain_inner_auth_list = lc.query(filter="(zimbraAuthMech=zimbra)", retrieve_attributes=None, base='', scope=ldap.SCOPE_SUBTREE)
"""
- Внешняя (через AD) аутентификация - zimbraAuthMech=ad. Нельзя менять пароль.
- Внутренняя аутентификация - zimbraAuthMech=zimbra. Можно менять пароль в интерфейсе.
- Эти записи в списке должны внешне отличаться
"""

# 3. Список пользователей на сервере
user_list = list(lc.query(filter="(objectClass=zimbraAccount)", retrieve_attributes=None, base='', scope=ldap.SCOPE_SUBTREE))
system_user_list = list(lc.query(filter="(zimbraIsSystemResource=TRUE)", retrieve_attributes=None, base='', scope=ldap.SCOPE_SUBTREE))
"""
С его помощью можно вытащить список только обычных пользователей
"""

# 4. Смена пароля
"""
user_uid = 'uid=lehamaaan,ou=people,dc=chukreev,dc=com'
user_node = lc.get_ldap_node(user_uid)
user_node.set_password(new_password)
lc._lo.passwd_s(user_uid, None, new_password)
# Для того, чтобы пользователя выбрасывало из почтового веб-интерфейса надо изменять параметр
zimbraAuthTokenValidityValue (всегда прибавлять 1)
# Далее надо сбросить кэш зимбры для пользователя
rsh root@10.100.1.66 /opt/zimbra/bin/zmprov flushcache account lehamaaan@chukreev.com
# Разобраться со сбросом кэша из ldap команды
"""

# 5. Изменение атрибутов учетной записи
"""
mod_attrs = [(ldap.MOD_REPLACE, 'userAccountControl', "546")]
                l.modify_s(dn,mod_attrs)
"""

# 6. Списки рассылки (список)
"""
distribution_list = list(lc.query(filter="(objectClass=zimbraDistributionList)", retrieve_attributes=None, base='', scope=ldap.SCOPE_SUBTREE))
#Список ящиков в рассылке
forward_list = res[0][1]['zimbraMailForwardingAddress']
"""

# 7. Псевдонимы (список) + редактирование в карточке
"""
alias_list = list(lc.query(filter="(objectClass=zimbraAlias)", retrieve_attributes=None, base='', scope=ldap.SCOPE_SUBTREE))
#Доступ к реальным адресам через alias.zimbraAliasTargetId=account.zimbraId
#Надо отфильтровать системные и не показывать их
# В карточке аккаунта доступ к алиасам сделать через поле mail и джоин к списку алиасов
"""

# 8. Пересылка (у конкретного ящика)
"""
user_uid = 'uid=lehamaaan,ou=people,dc=chukreev,dc=com'
user_node = lc.get_ldap_node(user_uid)
user_node.zimbraPrefMailForwardingAddress = '1@example.com, 2@exmaple.com'
user_node.zimbraMailForwardingAddress = ['4@example.com', '6@example.com']
У аккаунта есть 2 вида пересылки:
Видимые пользователю - zimbraPrefMailForwardingAddress - здесь адреса через запятую (текстовое поле)
Невидимые пользователю - zimbraMailForwardingAddress - здесь список адресов
"""

# 9. Удаление аккаунта
"""
dn = 'uid=user,ou=people,dc=f-heads,dc=test'
lc.delete(dn)
# Также необходимо удалить:
# 1) Все псевдонимы alias.zimbraAliasTargetId=account.zimbraId
# 2) Удалить из всех списков рассылки
delivery_list = lc.query(filter="(&(objectClass=zimbraDistributionList)(zimbraMailForwardingAddress=user@f-heads.test))",
                         retrieve_attributes=None, base='', scope=ldap.SCOPE_SUBTREE)
for delivery in delivery_list:
    current_account_list = delivery.zimbraMailForwardingAddress
    current_account_list.remove('user@f-heads.test')
    delivery.zimbraMailForwardingAddress = current_account_list
    delivery.save()
"""

# 10. Удаление псевдонима
"""
# 1) Удалить из аккаунтов account.zimbraMailAlias
# 2) Удалить из списков рассылки delivery.zimbraMailForwardingAddress
"""

# 11. Удаление списка рассылки
"""
Просто удаляется список рассылки и все, другие данные не тянутся
"""

# 12. Смена статуса аккаунта
"""
zimbraAccountStatus = (
    Активна - active
    Заблокирована - locked
    Закрыта - closed
    Ждет решения - pending
    Обслуживание - maintenance
)
"""

## Get full schema from DN specified in `base`
#result = lc.query()

## Select single node
node = lc.get_ldap_node('uid=lehamaaan,ou=people,dc=chukreev,dc=com')
#print node
#print node.sn

#node.sn = u'Чукреев Алексей' # change givenname
#node.save() # save all change
#print node sn # Unicode BUG FIXME
#node.delete() # delete