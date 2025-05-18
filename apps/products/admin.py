from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.products.models import Product, ProductImage, ProductFeature


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    min_num = 1


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    # inlines = [ProductImageInline, ProductFeatureInline]
    # readonly_fields = ('price', 'old_price','seen_count')
    # search_fields = ['seen_count','title']
    readonly_fields = ('seen_count',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass
