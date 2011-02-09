import types

from django.utils.http import urlquote  as django_urlquote
from django.utils.http import urlencode as django_urlencode
from django.utils.datastructures import MultiValueDict
from django.conf import settings


def urlquote(link=None, get={}):
    u'''
    This method does both: urlquote() and urlencode()

    urlqoute(): Quote special characters in 'link'

    urlencode(): Map dictionary to query string key=value&...

    HTML escaping is not done.

    Example:

      urlquote('/wiki/Python_(programming_language)')     --> '/wiki/Python_%28programming_language%29'
      urlquote('/mypath/', {'key': 'value'})              --> '/mypath/?key=value'
      urlquote('/mypath/', {'key': ['value1', 'value2']}) --> '/mypath/?key=value1&key=value2'
      urlquote({'key': ['value1', 'value2']})             --> 'key=value1&key=value2'
    '''
    assert link or get
    if isinstance(link, dict):
        # urlqoute({'key': 'value', 'key2': 'value2'}) --> key=value&key2=value2
        assert not get, get
        get=link
        link=''
    assert isinstance(get, dict), 'wrong type "%s", dict required' % type(get)
    #assert not (link.startswith('http://') or link.startswith('https://')), \
    #    'This method should only quote the url path. It should not start with http(s)://  (%s)' % (
    #    link)
    if get:
        # http://code.djangoproject.com/ticket/9089
        if isinstance(get, MultiValueDict):
            get=get.lists()
        if link:
            link='%s?' % django_urlquote(link)
        return u'%s%s' % (link, django_urlencode(get, doseq=True))
    else:
        return django_urlquote(link)


def return_attrib(obj, attrib, arguments={}):
    try:
        if isinstance(obj, types.DictType) or isinstance(obj, types.DictionaryType):
            return obj[attrib]
        elif isinstance(attrib, types.FunctionType):
            return attrib(obj)
        else:
            result = reduce(getattr, attrib.split("."), obj)
            if isinstance(result, types.MethodType):
                if arguments:
                    return result(**arguments)
                else:
                    return result()
            else:
                return result
    except Exception, err:
        if settings.DEBUG:
            return "Attribute error: %s; %s" % (attrib, err)
        else:
            pass


#http://snippets.dzone.com/posts/show/5434
#http://snippets.dzone.com/user/jakob
def pretty_size(size):
	suffixes = [("B",2**10), ("K",2**20), ("M",2**30), ("G",2**40), ("T",2**50)]
	for suf, lim in suffixes:
		if size > lim:
			continue
		else:
			return round(size/float(lim/2**10),2).__str__()+suf
