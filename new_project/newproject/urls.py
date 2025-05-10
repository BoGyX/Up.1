from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from hello.views import (
    index, about, contacts, map_view, categories, catalog, cart,
    add_to_cart, update_cart, clear_cart,
    register, login_view, logout_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('map/', map_view, name='map'),
    path('categories/', categories, name='categories'),
    path('catalog/', catalog, name='catalog'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>/', update_cart, name='update_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('api/', include('apishka.urls')),  # Исправлено: строковый путь
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)