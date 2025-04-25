from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from apps.general.views import (
    set_language,
    home,
    search,
    set_currency,
    page_404,
    clear_session,
)

# No-i18n routes (tilsiz URLlar)
urlpatterns = [
    path("__ckeditor5/", include('django_ckeditor_5.urls')),
    path('set-language/<str:lang>/', set_language, name='set-lang'),
    path('set-currency/<str:currency>/', set_currency, name='set-currency'),
]

# i18n URLlar (masalan, /en/, /uz/ bilan)
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

# Static & media fayllar faqat debug rejimda ko‘rsatiladi
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
