from django.contrib import admin
from .models import Book, SiteUser

# Register your models here.
admin.site.register(Book)
admin.site.register(SiteUser)
