"""
URL configuration for newproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hello.views import (
    index, about, contacts, map_view, categories, catalog, cart,
    MusicListView, MusicDetailView,
    MusicCreateView, MusicUpdateView, MusicDeleteView
)

urlpatterns = [
     path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('map/', map_view, name='map'),
    path('categories/', categories, name='categories'),
    path('catalog/', catalog, name='catalog'),
    path('cart/', cart, name='cart'),
    # Music views
    path('music/', MusicListView.as_view(), name='music_list'),
    path('music/<int:pk>/', MusicDetailView.as_view(), name='music_detail'),
    path('music/create/', MusicCreateView.as_view(), name='music_create'),
    path('music/<int:pk>/update/', MusicUpdateView.as_view(), name='music_update'),
    path('music/<int:pk>/delete/', MusicDeleteView.as_view(), name='music_delete'),
]

