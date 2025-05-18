from modeltranslation.translator import translator, TranslationOptions
from .models import Service

class GeneralTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Service, GeneralTranslationOptions)