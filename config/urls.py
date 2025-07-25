from django.contrib import admin
from django.conf import settings
from django.urls import path, include, reverse
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.http import HttpResponse

from apps.products.models import Product
from apps.general.views import (
    set_language,
    home,
    search,
    set_currency,
    page_404,
    clear_session,
)

# --- SITEMAPS ---
class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return [
            'home-page',
            'search',
            'about:about-page',
            'contacts:contact-page',
            'wishlists:wishlist',
            'carts:cart-page',
            'categories:category',
            'clear_session',
            '404-page',
        ]

    def location(self, item):
        try:
            return reverse(item)
        except:
            # Log or handle the error properly in production
            return "/"


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return reverse('products:detail-page', kwargs={'pk': obj.pk})


sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
}

# --- ROBOTS.TXT ---
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow:",
        "Sitemap: https://shinam-makon.uz/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# --- No-i18n routes ---
urlpatterns = [
    path("sitemap.xml", sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path("robots.txt", robots_txt),
    path("__ckeditor5/", include('django_ckeditor_5.urls')),
    path('set-language/<str:lang>/', set_language, name='set-lang'),
    path('set-currency/<str:currency>/', set_currency, name='set-currency'),
]

# --- i18n routes ---
urlpatterns += i18n_patterns(
    path('', home, name='home-page'),
    path('admin/', admin.site.urls),
    path('search/', search, name='search'),
    path('clear-session/', clear_session, name='clear_session'),

    path('category/', include('apps.categories.urls', namespace='categories')),
    path('checkout/', include('apps.orders.urls', namespace='checkouts')),
    path('contact/', include('apps.contact.urls', namespace='contacts')),
    path('about/', include('apps.abouts.urls', namespace='about')),
    path('wishlist/', include('apps.wishlist.urls', namespace='wishlists')),
    path('cart/', include('apps.cart.urls', namespace='carts')),
    path('coupons/', include('apps.coupons.urls', namespace='coupons')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('comments/', include('apps.comments.urls', namespace='comments')),
    path('subscribe/', include('apps.newsletter.urls', namespace='subscribers')),
    path('auth/', include('apps.authentication.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('404/', page_404, name='404-page'),
)

# --- Media va Static fayllar ---
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
