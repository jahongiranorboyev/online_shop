from modeltranslation.translator import translator, TranslationOptions
from .models import Product

class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'long_description', 'short_description')

translator.register(Product, ProductTranslationOptions)
