from modeltranslation.translator import translator, TranslationOptions

from .models import News
from ..banner.models import HeaderDiscount


class NewsTranslationOptions(TranslationOptions):
    fields = ['title', 'description']


class HeaderDiscountTranslationOptions(TranslationOptions):
    fields = ['text']


translator.register(HeaderDiscount, HeaderDiscountTranslationOptions)
translator.register(News, NewsTranslationOptions)
