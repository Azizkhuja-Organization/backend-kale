from modeltranslation.translator import translator, TranslationOptions

from .models import HeaderDiscount


class HeaderDiscountTranslationOptions(TranslationOptions):
    fields = ['text']


translator.register(HeaderDiscount, HeaderDiscountTranslationOptions)
