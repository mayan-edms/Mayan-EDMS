from django.conf import settings

#Theme options are:
#amro, bec, bec-green, blue, default, djime-cerulean, drastic-dark,
#kathleene, olive, orange, red, reidb-greenish, warehouse

THEME = getattr(settings, 'WEB_THEME', 'default')
