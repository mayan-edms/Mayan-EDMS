# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import re
import types
import tempfile
import string
import random

from django.utils.http import urlquote  as django_urlquote
from django.utils.http import urlencode as django_urlencode
from django.utils.datastructures import MultiValueDict
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


def urlquote(link=None, get=None):
    u"""
    This method does both: urlquote() and urlencode()

    urlqoute(): Quote special characters in 'link'

    urlencode(): Map dictionary to query string key=value&...

    HTML escaping is not done.

    Example:

      urlquote('/wiki/Python_(programming_language)')     --> '/wiki/Python_%28programming_language%29'
      urlquote('/mypath/', {'key': 'value'})              --> '/mypath/?key=value'
      urlquote('/mypath/', {'key': ['value1', 'value2']}) --> '/mypath/?key=value1&key=value2'
      urlquote({'key': ['value1', 'value2']})             --> 'key=value1&key=value2'
    """
    if get is None:
        get = []

    assert link or get
    if isinstance(link, dict):
        # urlqoute({'key': 'value', 'key2': 'value2'}) --> key=value&key2=value2
        assert not get, get
        get = link
        link = ''
    assert isinstance(get, dict), u'wrong type "%s", dict required' % type(get)
    #assert not (link.startswith('http://') or link.startswith('https://')), \
    #    'This method should only quote the url path.
    #    It should not start with http(s)://  (%s)' % (
    #    link)
    if get:
        # http://code.djangoproject.com/ticket/9089
        if isinstance(get, MultiValueDict):
            get = get.lists()
        if link:
            link = u'%s?' % django_urlquote(link)
        return u'%s%s' % (link, django_urlencode(get, doseq=True))
    else:
        return django_urlquote(link)


def return_attrib(obj, attrib, arguments=None):
    try:
        if isinstance(attrib, types.FunctionType):
            return attrib(obj)
        elif isinstance(obj, types.DictType) or isinstance(obj, types.DictionaryType):
            return obj[attrib]
        else:
            result = reduce(getattr, attrib.split(u'.'), obj)
            if isinstance(result, types.MethodType):
                if arguments:
                    return result(**arguments)
                else:
                    return result()
            else:
                return result
    except Exception, err:
        if settings.DEBUG:
            return 'Attribute error: %s; %s' % (attrib, err)
        else:
            pass


#http://snippets.dzone.com/posts/show/5434
#http://snippets.dzone.com/user/jakob
def pretty_size(size, suffixes=None):
    suffixes = suffixes if not suffixes is None else [
        (u'B', 1024L), (u'K', 1048576L), (u'M', 1073741824L),
        (u'G', 1099511627776L), (u'T', 1125899906842624L)
    ]

    for suf, lim in suffixes:
        if size > lim:
            continue
        else:
            try:
                return round(size / float(lim / 1024L), 2).__str__() + suf
            except ZeroDivisionError:
                return 0


def pretty_size_10(size):
    return pretty_size(
        size,
        suffixes=[
            (u'B', 1000L), (u'K', 1000000L), (u'M', 1000000000L),
            (u'G', 1000000000000L), (u'T', 1000000000000000L)
        ])


# The code here is based loosely on John Cardinal's notes found at:
# http://www.johncardinal.com/tmgutil/capitalizenames.htm

def proper_name(name):
    """
    Does the work of capitalizing a name (can be a full name).
    """
    mc = re.compile(r'^Mc(\w)(?=\w)', re.I)
    mac = re.compile(r'^Mac(\w)(?=\w)', re.I)
    suffixes = [
        u"II", u"(II)", u"III", u"(III)", u"IV", u"(IV)", u"VI", u"(VI)",
        u"VII", u"(VII)", u"2nd", u"(2nd)", u"3rd", u"(3rd)", u"4th", u"(4th)",
        u"5th", u"(5th)"
    ]

    # The names listed here are included by permission from John Cardinal's TMG Utility.
    # http://www.johncardinal.com/tmgutil/index.htm
    # John Cardinal maintains the copyright for this list of names.
    surnames = [
        u"ApShaw", u"d'Albini", "d'Aubigney", u"d'Aubigné", u"d'Autry",
        u"d'Entremont", u"d'Hurst", u"D'ovidio", u"da Graça", u"DaSilva",
        u"DeAnda", u"deAnnethe", u"deAubigne", u"deAubigny", u"DeBardelaben",
        u"DeBardeleben", u"DeBaugh", u"deBeauford", u"DeBerry", u"deBethune",
        u"DeBetuile", u"DeBoard", u"DeBoer", u"DeBohun", u"DeBord", u"DeBose",
        u"DeBrouwer", u"DeBroux", u"DeBruhl", u"deBruijn", u"deBrus", u"deBruse",
        u"deBrusse", u"DeBruyne", u"DeBusk", u"DeCamp", u"deCastilla", u"DeCello",
        u"deClare", u"DeClark", u"DeClerck", u"DeCoste", u"deCote", u"DeCoudres",
        u"DeCoursey", u"DeCredico", u"deCuire", u"DeCuyre", u"DeDominicios",
        u"DeDuyster", u"DeDuytscher", u"DeDuytser", u"deFiennes", u"DeFord",
        u"DeForest", u"DeFrance", u"DeFriece", u"DeGarmo", u"deGraaff", u"DeGraff",
        u"DeGraffenreid", u"DeGraw", u"DeGrenier", u"DeGroats", u"DeGroft",
        u"DeGrote", u"DeHaan", u"DeHaas", u"DeHaddeclive", u"deHannethe",
        u"DeHatclyf", u"DeHaven", u"DeHeer", u"DeJager", u"DeJarnette", u"DeJean",
        u"DeJong", u"deJonge", u"deKemmeter", u"deKirketon", u"DeKroon",
        u"deKype", u"del-Rosario", u"dela Chamotte", u"DeLa Cuadra",
        u"DeLa Force", u"dela Fountaine", u"dela Greña", u"dela Place",
        u"DeLa Ward", u"DeLaci", u"DeLacy", u"DeLaet", u"DeLalonde", u"DelAmarre",
        u"DeLancey", u"DeLascy", u"DelAshmutt", u"DeLassy", u"DeLattre",
        u"DeLaughter", u"DeLay", u"deLessine", u"DelGado", u"DelGaudio",
        u"DeLiberti", u"DeLoache", u"DeLoatch", u"DeLoch", u"DeLockwood",
        u"DeLong", u"DeLozier", u"DeLuca", u"DeLucenay", u"deLucy", u"DeMars",
        u"DeMartino", u"deMaule", u"DeMello", u"DeMinck", u"DeMink", u"DeMoree",
        u"DeMoss", u"DeMott", u"DeMuynck", u"deNiet", u"DeNise", u"DeNure",
        u"DePalma", u"DePasquale", u"dePender", u"dePercy", u"DePoe", u"DePriest",
        u"DePu", u"DePui", u"DePuis", u"DeReeper", u"deRochette", u"deRose",
        u"DeRossett", u"DeRover", u"deRuggele", u"deRuggle", u"DeRuyter",
        u"deSaint-Sauveur", u"DeSantis", u"desCuirs", u"DeSentis", u"DeShane",
        u"DeSilva", u"DesJardins", u"DesMarest", u"deSoleure", u"DeSoto",
        u"DeSpain", u"DeStefano", u"deSwaert", u"deSwart", u"DeVall", u"DeVane",
        u"DeVasher", u"DeVasier", u"DeVaughan", u"DeVaughn", u"DeVault", u"DeVeau",
        u"DeVeault", u"deVilleneuve", u"DeVilliers", u"DeVinney", u"DeVito",
        u"deVogel", u"DeVolder", u"DeVolld", u"DeVore", u"deVos", u"DeVries",
        u"deVries", u"DeWall", u"DeWaller", u"DeWalt", u"deWashington",
        u"deWerly", u"deWessyngton", u"DeWet", u"deWinter", u"DeWitt", u"DeWolf",
        u"DeWolfe", u"DeWolff", u"DeWoody", u"DeYager", u"DeYarmett", u"DeYoung",
        u"DiCicco", u"DiCredico", u"DiFillippi", u"DiGiacomo", u"DiMarco",
        u"DiMeo", u"DiMonte", u"DiNonno", u"DiPietro", u"diPilato", u"DiPrima",
        u"DiSalvo", u"du Bosc", u"du Hurst", u"DuFort", u"DuMars", u"DuPre",
        u"DuPue", u"DuPuy", u"FitzUryan", u"kummel", u"LaBarge", u"LaBarr",
        u"LaBauve", u"LaBean", u"LaBelle", u"LaBerteaux", u"LaBine", u"LaBonte",
        u"LaBorde", u"LaBounty", u"LaBranche", u"LaBrash", u"LaCaille", u"LaCasse",
        u"LaChapelle", u"LaClair", u"LaComb", u"LaCoste", u"LaCount", u"LaCour",
        u"LaCroix", u"LaFarlett", u"LaFarlette", u"LaFerry", u"LaFlamme",
        u"LaFollette", u"LaForge", u"LaFortune", u"LaFoy", u"LaFramboise",
        u"LaFrance", u"LaFuze", u"LaGioia", u"LaGrone", u"LaLiberte", u"LaLonde",
        u"LaLone", u"LaMaster", u"LaMay", u"LaMere", u"LaMont", u"LaMotte",
        u"LaPeer", u"LaPierre", u"LaPlante", u"LaPoint", u"LaPointe", u"LaPorte",
        u"LaPrade", u"LaRocca", u"LaRochelle", u"LaRose", u"LaRue", u"LaVallee",
        u"LaVaque", u"LaVeau", u"LeBleu", u"LeBoeuf", u"LeBoiteaux", u"LeBoyteulx",
        u"LeCheminant", u"LeClair", u"LeClerc", u"LeCompte", u"LeCroy", u"LeDuc",
        u"LeFevbre", u"LeFever", u"LeFevre", u"LeFlore", u"LeGette", u"LeGrand",
        u"LeGrave", u"LeGro", u"LeGros", u"LeJeune", u"LeMaistre", u"LeMaitre",
        u"LeMaster", u"LeMesurier", u"LeMieux", u"LeMoe", u"LeMoigne", u"LeMoine",
        u"LeNeve", u"LePage", u"LeQuire", u"LeQuyer", u"LeRou", u"LeRoy", u"LeSuer",
        u"LeSueur", u"LeTardif", u"LeVally", u"LeVert", u"LoMonaco", u"Macabe",
        u"Macaluso", u"MacaTasney", u"Macaulay", u"Macchitelli", u"Maccoone",
        u"Maccurry", u"Macdermattroe", u"Macdiarmada", u"Macelvaine", u"Macey",
        u"Macgraugh", u"Machan", u"Machann", u"Machum", u"Maciejewski", u"Maciel",
        u"Mackaben", u"Mackall", u"Mackartee", u"Mackay", u"Macken", u"Mackert",
        u"Mackey", u"Mackie", u"Mackin", u"Mackins", u"Macklin", u"Macko",
        u"Macksey", u"Mackwilliams", u"Maclean", u"Maclinden", u"Macomb",
        u"Macomber", u"Macon", u"Macoombs", u"Macraw", u"Macumber", u"Macurdy",
        u"Macwilliams", u"MaGuinness", u"MakCubyn", u"MakCumby", u"Mcelvany",
        u"Mcsherry", u"Op den Dyck", u"Op den Graeff", u"regory", u"Schweißguth",
        u"StElmo", u"StGelais", u"StJacques", u"te Boveldt", u"VanAernam",
        u"VanAken", u"VanAlstine", u"VanAmersfoort", u"VanAntwerp", u"VanArlem",
        u"VanArnam", u"VanArnem", u"VanArnhem", u"VanArnon", u"VanArsdale",
        u"VanArsdalen", u"VanArsdol", u"vanAssema", u"vanAsten", u"VanAuken",
        u"VanAwman", u"VanBaucom", u"VanBebber", u"VanBeber", u"VanBenschoten",
        u"VanBibber", u"VanBilliard", u"vanBlare", u"vanBlaricom", u"VanBuren",
        u"VanBuskirk", u"VanCamp", u"VanCampen", u"VanCleave", u"VanCleef",
        u"VanCleve", u"VanCouwenhoven", u"VanCovenhoven", u"VanCowenhoven",
        u"VanCuren", u"VanDalsem", u"VanDam", u"VanDe Poel", u"vanden Dijkgraaf",
        u"vanden Kommer", u"VanDer Aar", u"vander Gouwe", u"VanDer Honing",
        u"VanDer Hooning", u"vander Horst", u"vander Kroft", u"vander Krogt",
        u"VanDer Meer", u"vander Meulen", u"vander Putte", u"vander Schooren",
        u"VanDer Veen", u"VanDer Ven", u"VanDer Wal", u"VanDer Weide",
        u"VanDer Willigen", u"vander Wulp", u"vander Zanden", u"vander Zwan",
        u"VanDer Zweep", u"VanDeren", u"VanDerlaan", u"VanDerveer",
        u"VanderWoude", u"VanDeursen", u"VanDeusen", u"vanDijk", u"VanDoren",
        u"VanDorn", u"VanDort", u"VanDruff", u"VanDryer", u"VanDusen", u"VanDuzee",
        u"VanDuzen", u"VanDuzer", u"VanDyck", u"VanDyke", u"VanEman", u"VanEmmen",
        u"vanEmmerik", u"VanEngen", u"vanErp", u"vanEssen", u"VanFleet",
        u"VanGalder", u"VanGelder", u"vanGerrevink", u"VanGog", u"vanGogh",
        u"VanGorder", u"VanGordon", u"VanGroningen", u"VanGuilder", u"VanGundy",
        u"VanHaaften", u"VanHaute", u"VanHees", u"vanHeugten", u"VanHise",
        u"VanHoeck", u"VanHoek", u"VanHook", u"vanHoorn", u"VanHoornbeeck",
        u"VanHoose", u"VanHooser", u"VanHorn", u"VanHorne", u"VanHouten",
        u"VanHoye", u"VanHuijstee", u"VanHuss", u"VanImmon", u"VanKersschaever",
        u"VanKeuren", u"VanKleeck", u"VanKoughnet", u"VanKouwenhoven",
        u"VanKuykendaal", u"vanLeeuwen", u"vanLent", u"vanLet", u"VanLeuven",
        u"vanLingen", u"VanLoozen", u"VanLopik", u"VanLuven", u"vanMaasdijk",
        u"VanMele", u"VanMeter", u"vanMoorsel", u"VanMoorst", u"VanMossevelde",
        u"VanNaarden", u"VanNamen", u"VanNemon", u"VanNess", u"VanNest",
        u"VanNimmen", u"vanNobelen", u"VanNorman", u"VanNormon", u"VanNostrunt",
        u"VanNote", u"VanOker", u"vanOosten", u"VanOrden", u"VanOrder",
        u"VanOrma", u"VanOrman", u"VanOrnum", u"VanOstrander", u"VanOvermeire",
        u"VanPelt", u"VanPool", u"VanPoole", u"VanPoorvliet", u"VanPutten",
        u"vanRee", u"VanRhijn", u"vanRijswijk", u"VanRotmer", u"VanSchaick",
        u"vanSchelt", u"VanSchoik", u"VanSchoonhoven", u"VanSciver", u"VanScoy",
        u"VanScoyoc", u"vanSeters", u"VanSickle", u"VanSky", u"VanSnellenberg",
        u"vanStaveren", u"VanStraten", u"VanSuijdam", u"VanTassel", u"VanTassell",
        u"VanTessel", u"VanTexel", u"VanTuyl", u"VanValckenburgh", u"vanValen",
        u"VanValkenburg", u"VanVelsor", u"VanVelzor", u"VanVlack", u"VanVleck",
        u"VanVleckeren", u"VanWaard", u"VanWart", u"VanWassenhove", u"VanWinkle",
        u"VanWoggelum", u"vanWordragen", u"VanWormer", u"VanZuidam",
        u"VanZuijdam", u"VonAdenbach", u"vonAllmen", u"vonBardeleben",
        u"vonBerckefeldt", u"VonBergen", u"vonBreyman", u"VonCannon",
        u"vonFreymann", u"vonHeimburg", u"VonHuben", u"vonKramer",
        u"vonKruchenburg", u"vonPostel", u"VonRohr", u"VonRohrbach",
        u"VonSass", u"VonSasse", u"vonSchlotte", u"VonSchneider", u"VonSeldern",
        u"VonSpringer", u"VonVeyelmann", u"VonZweidorff"
    ]

    hyphen_indexes = []
    while name.find(u'-') > -1:
        index = name.find(u'-')
        hyphen_indexes.append(index)
        name = name[:index] + u' ' + name[index + 1:]
    name = name.split()
    name = [w.capitalize() for w in name]  # standard capitalization
    # "Mcx" should be "McX"
    index = 0
    for w in name:
        try:
            name[index] = mc.sub(u'Mc' + w[2].upper(), w)
        except:
            pass
        index += 1
    # "Macx" should be "MacX"
    index = 0
    for w in name:
        try:
            name[index] = mac.sub(u'Mac' + w[3].upper(), w)
        except:
            pass
        index += 1
    name = u' '.join(name)
    for index in hyphen_indexes:
        name = name[:index] + u'-' + name[index + 1:]

    # funky stuff (no capitalization)
    name = name.replace(u' Dit ', u' dit ')
    name = name.replace(u' Van ', u' van ')
    name = name.replace(u' De ', u' de ')

    # special surnames and suffixes
    name += u' '
    for surname in surnames + suffixes:
        pos = name.lower().find(surname.lower())
        if pos > -1:
            # surname/suffix must be:
            # 1. at start of name or after a space
            #          -and-
            # 2. followed by the end of string or a space
            if (((pos == 0) or (pos > 0 and name[pos - 1] == u' '))
                and ((len(name) == pos + len(surname))
                or (name[pos + len(surname)] == u' '))):
                name = name[:pos] + surname + name[pos + len(surname):]
    return name.strip()


def return_type(value):
    if isinstance(value, types.FunctionType):
        return value.__doc__ if value.__doc__ else _(u'function found')
    elif isinstance(value, types.ClassType):
        return u'%s.%s' % (value.__class__.__module__, value.__class__.__name__)
    elif isinstance(value, types.TypeType):
        return u'%s.%s' % (value.__module__, value.__name__)
    elif isinstance(value, types.DictType) or isinstance(value, types.DictionaryType):
        return u', '.join(list(value))
    else:
        return value


# http://stackoverflow.com/questions/4248399/page-range-for-printing-algorithm
def parse_range(astr):
    result = set()
    for part in astr.split(u','):
        x = part.split(u'-')
        result.update(range(int(x[0]), int(x[-1]) + 1))
    return sorted(result)


def generate_choices_w_labels(choices, display_object_type=True):
    results = []
    for choice in choices:
        ct = ContentType.objects.get_for_model(choice)
        label = unicode(choice)
        if isinstance(choice, User):
            label = choice.get_full_name() if choice.get_full_name() else choice

        if display_object_type:
            verbose_name = unicode(getattr(choice._meta, u'verbose_name', ct.name))
            results.append((u'%s,%s' % (ct.model, choice.pk), u'%s: %s' % (verbose_name, label)))
        else:
            results.append((u'%s,%s' % (ct.model, choice.pk), u'%s' % (label)))

    #Sort results by the label not the key value
    return sorted(results, key=lambda x: x[1])


def get_object_name(obj, display_object_type=True):
    ct_label = ContentType.objects.get_for_model(obj).name
    if isinstance(obj, User):
        label = obj.get_full_name() if obj.get_full_name() else obj
    else:
        label = unicode(obj)

    if display_object_type:
        try:
            verbose_name = unicode(obj._meta.verbose_name)
        except AttributeError:
            verbose_name = ct_label

        return u'%s: %s' % (verbose_name, label)
    else:
        return u'%s' % (label)


def return_diff(old_obj, new_obj, attrib_list=None):
    diff_dict = {}
    if not attrib_list:
        attrib_list = old_obj.__dict__.keys()
    for attrib in attrib_list:
        old_val = getattr(old_obj, attrib)
        new_val = getattr(new_obj, attrib)
        if old_val != new_val:
            diff_dict[attrib] = {
                'old_value': old_val,
                'new_value': new_val
            }

    return diff_dict


def validate_path(path):
    if os.path.exists(path) != True:
        # If doesn't exist try to create it
        try:
            os.mkdir(path)
        except:
            return False

    # Check if it is writable
    try:
        fd, test_filepath = tempfile.mkstemp(dir=path)
        os.close(fd)
        os.unlink(test_filepath)
    except:
        return False

    return True


def encapsulate(function):
    # Workaround Django ticket 15791
    # Changeset 16045
    # http://stackoverflow.com/questions/6861601/cannot-resolve-callable-context-variable/6955045#6955045
    return lambda: function


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def get_descriptor(file_input, read=True):
    try:
        # Is it a file like object?
        file_input.seek(0)
    except AttributeError:
        # If not, try open it.
        if read:
            return open(file_input, 'rb')
        else:
            return open(file_input, 'wb')
    else:
        return file_input


#http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
def copyfile(source, destination, buffer_size=1024 * 1024):
    """
    Copy a file from source to dest. source and dest
    can either be strings or any object with a read or
    write method, like StringIO for example.
    """
    source_descriptor = get_descriptor(source)
    destination_descriptor = get_descriptor(destination, read=False)

    while True:
        copy_buffer = source_descriptor.read(buffer_size)
        if copy_buffer:
            destination_descriptor.write(copy_buffer)
        else:
            break

    source_descriptor.close()
    destination_descriptor.close()
