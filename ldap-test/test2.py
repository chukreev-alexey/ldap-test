# -*- coding: utf-8 -*-

# python-ldap library test

from utils import ldapom

LDAP_HOST = '195.189.111.9'
LDAP_PORT = 4389

LDAP_USERNAME = 'uid=zimbra,cn=admins,cn=zimbra'
LDAP_PASSWORD = 'q_DXNyB0Ym'

server = 'ldap://%s:%d' % (LDAP_HOST, LDAP_PORT)



lc = ldapom.LdapConnection(uri=server, base='dc=chukreev,dc=com',
                           login=LDAP_USERNAME, password=LDAP_PASSWORD)

## Get full schema from DN specified in `base`
result = lc.query()

## Select single node
node = lc.get_ldap_node('uid=lehamaaan,ou=people,dc=chukreev,dc=com')
#print node
#print node.sn

#node.sn = u'Чукреев Алексей' # change givenname
#node.save() # save all change
#print node sn # Unicode BUG FIXME
#node.delete() # delete