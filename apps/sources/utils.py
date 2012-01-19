import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext


# From http://www.peterbe.com/plog/whitelist-blacklist-logic
def accept_item(value, whitelist, blacklist, default_accept=True):
    """
    return true if this item is either whitelisted or
    not blacklisted
    """
    if not whitelist:
        whitelist = []

    if not blacklist:
        blacklist = []

    # note the order
    for reject, item_list in ([False, whitelist], [True, blacklist]):
        #print 'item_list: %s' % item_list
        #print 'reject: %s' % reject
        for okpattern in item_list:
            #print 'okpattern: %s' % okpattern
            if re.findall(okpattern.replace('*', '\S+'), value, re.I):
                # match!
                #print 'MATCH'
                if reject:
                    return False
                else:
                    return True

    # default is to accept all
    return default_accept


def validate_whitelist_blacklist(value, whitelist, blacklist):
    #print 'blacklist', blacklist
    if not accept_item(value, whitelist, blacklist):
        raise ValidationError(ugettext(u'Whitelist Blacklist validation error.'))
