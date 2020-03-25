# Ensure this file is not saved as "ldap.py" or you will run
# into name conflicts (https://gitlab.com/mayan-edms/mayan-edms/issues/743)
# Install Python LDAP with:
# $ pip install python-ldap
# or if using Docker, pass the following environment variables:
# -e MAYAN_PIP_INSTALLS=python-ldap
# -e MAYAN_APT_INSTALLS=libsasl2-dev python3-dev libldap2-dev libssl-dev libgle3 build-essential autoconf libtool pkg-config gcc
# -e MAYAN_SETTINGS_MODULE=mayan_settings.ldap_connection_settings
import ldap

from django_auth_ldap.config import (
    LDAPSearch, LDAPSearchUnion, NestedActiveDirectoryGroupType
)

from mayan.settings.production import *  # NOQA

# Makes sure this works in Active Directory
ldap.set_option(ldap.OPT_REFERRALS, False)

# Turn of debug output, turn this off when everything is working as expected
ldap.set_option(ldap.OPT_DEBUG_LEVEL, 1)

# Default: True
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use TLS to talk to the LDAP server
# Requires acquiring the server's certificate
# $ openssl s_client -connect <LDAP server>:636
# Part of the output of this file will be the Base-64 encoded .cer file
# that was presented for LDAPS. Cut and paste into a file beginning at
# "-Begin Certificate" through "-End Certificate--" and save as a .crt, for
# example: ldapserver.crt
# $ CERT=ldapserver.crt
# $ cp /root/$CERT /usr/share/ca-certificates/$CERT
# # notice the + sign which tells to activate the certificate.
# $ echo "+$CERT" >/etc/ca-certificates/update.d/activate_my_cert
# $ dpkg-reconfigure ca-certificates;
AUTH_LDAP_START_TLS = False

LDAP_ADDITIONAL_USER_DN = 'dc=people'
LDAP_ADMIN_DN = ''
LDAP_BASE_DN = 'dc=<top level dc>,dc=co,dc=in'
LDAP_PASSWORD = ''
LDAP_USER_AUTO_CREATION = 'False'
LDAP_URL = 'ldap://<LDAP server>:389/'

AUTH_LDAP_BIND_DN = LDAP_ADMIN_DN
AUTH_LDAP_BIND_PASSWORD = LDAP_PASSWORD
AUTH_LDAP_SERVER_URI = LDAP_URL

# Simple search
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    '%s,%s' % (LDAP_ADDITIONAL_USER_DN, LDAP_BASE_DN),
    ldap.SCOPE_SUBTREE, '(uid=%(user)s)'
)

# If you need to search in more than one place for a user, you can use
# LDAPSearchUnion. This takes multiple LDAPSearch objects and returns the
# union of the results. The precedence of the underlying searches is
# unspecified.
# https://django-auth-ldap.readthedocs.io/en/latest/authentication.html
# AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
#     LDAPSearch(
#         'ou=Users,ou=Admin,dc=<top level DC>,dc=local', ldap.SCOPE_SUBTREE,
#         '(samaccountname=%(user)s)'
#     ),
#     LDAPSearch(
#         'ou=Users,ou=<second OU>,dc=<top level DC>,dc=local',
#         ldap.SCOPE_SUBTREE, '(samaccountname=%(user)s)'
#     ),
#     LDAPSearch(
#         'ou=Users,ou=<third OU>,dc=<top level DC>,dc=local',
#         ldap.SCOPE_SUBTREE, '(samaccountname=%(user)s)'
#     ),
# )

# User attributes to map from LDAP to Mayan's user model.
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'cn',
    'last_name': 'sn',
    'email': 'mail'
}
# Another example map
# AUTH_LDAP_USER_ATTR_MAP = {
#     'username': 'sAMAccountName',
#     'first_name': 'givenName',
#     'last_name': 'sn',
#     'email': 'mail'
# }
# Only string fields can be mapped to attributes. Boolean fields can be
# defined by group membership:
# AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#     'is_active': 'cn=active,ou=groups,dc=example,dc=com',
#     'is_staff': (
#         LDAPGroupQuery('cn=staff,ou=groups,dc=example,dc=com')
#         | LDAPGroupQuery('cn=admin,ou=groups,dc=example,dc=com')
#     ),
#     'is_superuser': 'cn=superuser,ou=groups,dc=example,dc=com',
# }

# Simple group search
# AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
#     'ou=groups,dc=example,dc=com', ldap.SCOPE_SUBTREE, '(objectClass=groupOfNames)'
# )
# AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

# Advanced group search
# AUTH_LDAP_GROUP_SEARCH = LDAPSearchUnion(
#     LDAPSearch(
#         'ou=Domain Global,OU=Security,OU=Groups,OU=<OU>,dc=<top level DC>,dc=local',
#         ldap.SCOPE_SUBTREE,
#         '(&(objectClass=group)(groupType:1.2.840.113556.1.4.803:=2147483648))'
#     ),
#     LDAPSearch(
#         'ou=Domain Global,OU=Security,OU=Groups,OU=<OU>,dc=<top level DC>,dc=local',
#         ldap.SCOPE_SUBTREE,
#         '(&(objectClass=group)(groupType:1.2.840.113556.1.4.803:=2147483648))'
#     ),
# )
# AUTH_LDAP_CACHE_GROUPS = True
# AUTH_LDAP_FIND_GROUP_PERMS = False
# AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType()
# AUTH_LDAP_MIRROR_GROUPS = True

# To minimize traffic to the LDAP server, LDAPBackend can make use of
# Django’s cache framework to keep a copy of a user’s LDAP group memberships.
# To enable this feature, set AUTH_LDAP_CACHE_TIMEOUT, which determines
# the timeout of cache entries in seconds.
# AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

# Limiting Access
# The simplest use of groups is to limit the users who are allowed to log in.
# If AUTH_LDAP_REQUIRE_GROUP is set, then only users who are members of that
# group will successfully authenticate. AUTH_LDAP_DENY_GROUP is the reverse:
# if given, members of this group will be rejected.
# AUTH_LDAP_REQUIRE_GROUP = 'cn=enabled,ou=groups,dc=example,dc=com'
# AUTH_LDAP_DENY_GROUP = 'cn=disabled,ou=groups,dc=example,dc=com'

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
)
