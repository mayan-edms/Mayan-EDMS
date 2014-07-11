# -*- coding: utf-8 -*-
import re


def check_word(word):
    ALL_ALPHANUM = re.compile('([0-9a-zäöüß])', re.I)
    NON_ALPHANUM = re.compile('([^0-9a-zäöüß])', re.I)
    ALL_ALPHANUM = re.compile('([0-9a-z])', re.I)
    NON_ALPHANUM = re.compile('([^0-9a-z])', re.I)

    TOO_MANY_VOWELS = re.compile('[aäeioöuü]{4}', re.I)
    TOO_MANY_CONSONANTS = re.compile('[bcdfghjklmnpqrstvwxyz]{4}', re.I)
    ALL_ALPHA = re.compile('^[a-z]+$', re.I)
    # SINGLE_LETTER_WORDS = re.compile('^$', re.I)

    #(L) If a string is longer than 40 characters, it is considered as garbage
    # http://www.duden.de/sprachwissen/sprachratgeber/die-laengsten-woerter-im-dudenkorpus
    # http://www.duden.de/sprachwissen/sprachratgeber/durchschnittliche-laenge-eines-deutschen-wortes
    if len(word) > 40:
        return None

    #(A) If a string's ratio of alphanumeric characters to total
    #characters is less than 50%, the string is garbage
    if len(ALL_ALPHANUM.findall(word)) < len(word) / 2:
        return None

    #Remove word if all the letters in the word are non alphanumeric
    if len(NON_ALPHANUM.findall(word)) == len(word):
        return None

    #Removed words with too many consecutie vowels
    if TOO_MANY_VOWELS.findall(word):
        return None

    #Removed words with too many consecutie consonants
    if TOO_MANY_CONSONANTS.findall(word):
        return None

    # No single letter words in German
    if len(word) == 1:
        return None

    return word
