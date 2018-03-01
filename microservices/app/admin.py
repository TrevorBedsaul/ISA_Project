from django.contrib import admin
from .models import Book, Buyer, Seller, GenericUser

# Register your models here.
admin.site.register(Book)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(GenericUser)
