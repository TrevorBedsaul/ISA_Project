"""services URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/books/(?P<book_id>\d+)$', views.get_book, name='get_book'),
    url(r'^api/v1/books/all$', views.get_all_books, name='get_all_books'),
    url(r'^api/v1/books/create$', views.create_book, name='create_book'),
    url(r'^api/v1/books/(?P<book_id>\d+)/update$', views.update_book, name='update_book'),
    url(r'^api/v1/books/(?P<book_id>\d+)/delete', views.delete_book, name='delete_book'),
]

urlpatterns += [
    url(r'^api/v1/sellers/(?P<seller_id>\d+)$', views.get_seller, name='get_seller'),
    url(r'^api/v1/sellers/(?P<seller_id>\d+)/update$', views.update_seller, name='update_seller'),
    url(r'^api/v1/sellers/create$', views.create_seller, name='create_seller'),
    url(r'^api/v1/sellers/(?P<seller_id>\d+)/delete', views.delete_seller, name='delete_seller'),
]

urlpatterns += [
    url(r'^api/v1/buyers/(?P<buyer_id>\d+)$', views.get_buyer, name='get_buyer'),
    url(r'^api/v1/buyers/(?P<buyer_id>\d+)/update$', views.update_buyer, name='update_buyer'),
    url(r'^api/v1/buyers/create$', views.create_buyer, name='create_buyer'),
    url(r'^api/v1/buyers/(?P<buyer_id>\d+)/delete', views.delete_buyer, name='delete_buyer'),
]
