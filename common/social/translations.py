from modeltranslation.translator import translator, TranslationOptions

from .models import Map


class MapTranslationOptions(TranslationOptions):
    fields = ['title', 'text']


translator.register(Map, MapTranslationOptions)
