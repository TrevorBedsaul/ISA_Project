from django.db import models
from django.core import serializers

# Create your models here.

class GenericUser(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    def convert_to_json(self):
        return serializers.serialize('json', self)


class Buyer(models.Model):
    generic_user = models.ForeignKey(GenericUser)
    address = models.CharField(max_length=200)
    rating = models.FloatField()
    activity_score = models.FloatField()
    def convert_to_json(self):
        return serializers.serialize('json', self)


class Seller(models.Model):
    generic_user = models.ForeignKey(GenericUser)
    rating = models.FloatField()
    activity_score = models.FloatField()
    def convert_to_json(self):
        return serializers.serialize('json', self)


class Book(models.Model):
    title = models.CharField(max_length=300)
    ISBN = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    price = models.FloatField()
    year = models.CharField(max_length=10)
    class_id = models.CharField(max_length=15)
    edition = models.IntegerField()

    AVAILABLE = "AV"
    IN_TRANSIT = "IT"
    DELIVERED = "DE"
    STATUS_CHOICES = (
        (AVAILABLE, "Available"),
        (IN_TRANSIT, "In Transit"),
        (DELIVERED, "Delivered"),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=AVAILABLE
    )

    HARDCOVER = "HC"
    PAPERBACK = "PB"
    LOOSE_LEAF = "LL"
    TYPE_CHOICES = (
        (HARDCOVER, "Hardcover"),
        (PAPERBACK, "Paperback"),
        (LOOSE_LEAF, "Loose leaf"),
    )
    type_name = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=HARDCOVER
    )

    NEW = "NW"
    USED_GOOD = "UG"
    USED_BAD = "UB"
    CONDITION_CHOICES = (
        (NEW, "New"),
        (USED_GOOD, "Used, in good condition"),
        (USED_BAD, "Used, in poor condition"),
    )
    condition = models.CharField(
        max_length=2,
        choices=CONDITION_CHOICES,
        default=NEW
    )

    seller = models.ForeignKey(Seller)
    buyer = models.ForeignKey(Buyer, null=True)
