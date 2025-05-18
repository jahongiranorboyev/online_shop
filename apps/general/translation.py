from modeltranslation.translator import translator, TranslationOptions
from .models import General

class GeneralTranslationOptions(TranslationOptions):
    fields = ('text', 'address',)

translator.register(General, GeneralTranslationOptions)