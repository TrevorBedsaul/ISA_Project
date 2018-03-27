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
    url(r'^api/v1/books$', views.get_book, name='get_book'),
    url(r'^api/v1/books/create$', views.create_book, name='create_book'),
    url(r'^api/v1/books/(?P<book_id>\d+)/update$', views.update_book, name='update_book'),
    url(r'^api/v1/books/(?P<book_id>\d+)/delete', views.delete_book, name='delete_book'),
]

urlpatterns += [
    url(r'^api/v1/users$', views.get_user, name='get_user'),
    url(r'^api/v1/users/(?P<user_id>\d+)/update$', views.update_user, name='update_user'),
    url(r'^api/v1/users/create$', views.create_user, name='create_user'),
    url(r'^api/v1/users/(?P<user_id>\d+)/delete', views.delete_user, name='delete_user'),
]

urlpatterns += [
    url(r'^api/v1/login$', views.login, name='login'),
    url(r'^api/v1/check_authenticator$', views.check_authenticator, name='check_authenticator'),
    url(r'^api/v1/logout', views.logout, name='logout'),
]
