from modeltranslation.translator import translator, TranslationOptions

from .models import Catalog


class CatalogTranslationOptions(TranslationOptions):
    fields = ['title', 'description']


translator.register(Catalog, CatalogTranslationOptions)
