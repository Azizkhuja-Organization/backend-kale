from modeltranslation.translator import translator, TranslationOptions

from .models import Portfolio


class PortfolioTranslationOptions(TranslationOptions):
    fields = ['title', 'description']


translator.register(Portfolio, PortfolioTranslationOptions)
