from django.utils import translation


def to_language(promise, language):
    current_language = translation.get_language()
    translation.activate(language=language)
    result = str(promise)
    translation.activate(language=current_language)

    return result
