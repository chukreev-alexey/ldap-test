# -*- coding: utf-8 -*-

# python-ldap library test

import ldap

LDAP_HOST = '195.189.111.9'
LDAP_PORT = 4389

LDAP_USERNAME = 'uid=zimbra,cn=admins,cn=zimbra'
LDAP_PASSWORD = 'q_DXNyB0Ym'

server = 'ldap://%s:%d' % (LDAP_HOST, LDAP_PORT)
con = ldap.initialize(server)
con.simple_bind_s(LDAP_USERNAME, LDAP_PASSWORD)

res = con.search_s('ou=people,dc=chukreev,dc=com', ldap.SCOPE_SUBTREE, '(uid=lehamaaan)',['cn','mail'])