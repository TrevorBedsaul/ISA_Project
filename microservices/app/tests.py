from django.test import TestCase, Client
from app.models import Book, Buyer, Seller, GenericUser
from django.core.urlresolvers import reverse


class TestBuyers(TestCase):

    def setUp(self):
        pass

    def testCreate(self):
        c = Client()
        response = c.post("/api/v1/buyers/create", {"name": "John Doe", "phone": "123456789", "email": "hello@gmail.com", "password": "pwd", "username": "JDoe", "address": "Earth", "rating": 9.0, "activity_score": 5.0})
        self.assertAlmostEquals(response.status_code, 201)

    def testRead(self):
        pass

        
    # def testUpdate(self):

    # def testDelete(self):

    # def tearDown(self):
        # pass
