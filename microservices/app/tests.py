from django.test import TestCase, Client
from .models import Book, Buyer, Seller, GenericUser
from django.core.urlresolvers import reverse


class TestBuyers(TestCase):

    def setUp(self):
        pass

    def testCreate(self):
        c = Client()
        response = c.post("/api/v1/buyers/create", {"name": "John Doe", "phone": "123456789", "email": "hello@gmail.com", "password": "pwd", "username": "JDoe", "address": "Earth", "rating": 9.0, "activity_score": 5.0})
        self.assertAlmostEquals(response.status_code, 201)

    def testRead(self):
        c = Client()
        response = c.get("api/v1/buyers/(?P<buyer_id>\d+)", kwargs={'buyer_id':1})
        self.assertAlmostEquals(response.status_code, 201)
        response2 = c.get("api/v1/buyers/(?P<buyer_id>\d+)", kwargs={'buyer_id':3})
        self.assertAlmostEquals(response2.status_code, 404)

    def testUpdate(self):
        c = Client()
        response = c.post("api/v1/buyers/(?P<buyer_id>\d+)/update", {"email": "newemail@yahoo.com"}, kwargs={'buyer_id':1})
        self.assertAlmostEquals(response.status_code, 201)

    def testDelete(self):
        c = Client()
        response = c.post("api/v1/buyers/(?P<buyer_id>\d+)/delete", kwargs={'buyer_id':1})
        self.assertAlmostEquals(response.status_code, 405)
        response2 = c.get("api/v1/buyers/(?P<buyer_id>\d+)/delete", kwargs={'buyer_id':1})
        self.assertAlmostEquals(response2.status_code, 201)

    def tearDown(self):
        pass


class TestSellers(TestCase):

    def setUp(self):
        pass

    def testCreateSeller(self):
        c = Client()
        response = c.post("/api/v1/sellers/create",
                          {"name": "Sarah Jane", "phone": "987654321", "email": "sjane@gmail.com", "password": "pass",
                           "username": "SJane", "rating": 7.5, "activity_score": 8.0})
        self.assertAlmostEquals(response.status_code, 201)

    def testReadSeller(self):
        c = Client()
        response = c.get("api/v1/sellers/(?P<seller_id>\d+)", kwargs={'seller_id': 1})
        self.assertAlmostEquals(response.status_code, 201)
        response2 = c.get("api/v1/sellers/(?P<seller_id>\d+)", kwargs={'seller_id': 3})
        self.assertAlmostEquals(response2.status_code, 404)

    def testUpdateSeller(self):
        c = Client()
        response = c.post("api/v1/sellers/(?P<seller_id>\d+)/update", {"email": "newemail@yahoo.com"},
                          kwargs={'seller_id': 1})
        self.assertAlmostEquals(response.status_code, 201)

    def testDeleteSeller(self):
        c = Client()
        response = c.post("api/v1/sellers/(?P<seller_id>\d+)/delete", kwargs={'seller_id': 1})
        self.assertAlmostEquals(response.status_code, 405)
        response2 = c.get("api/v1/sellers/(?P<seller_id>\d+)/delete", kwargs={'seller_id': 1})
        self.assertAlmostEquals(response2.status_code, 201)

    def tearDown(self):
        pass


class TestBooks(TestCase):

    def setUp(self):
        pass

    def testCreateBook(self):
        c = Client()
        response = c.post("/api/v1/sellers/create",
                          {"name": "Sarah Jane", "phone": "987654321", "email": "sjane@gmail.com", "password": "pass",
                           "username": "SJane", "rating": 7.5, "activity_score": 8.0})
        response = c.post("/api/v1/books/create",
                          {"title": "Intro to Politics", "ISBN": "343459789", "author": "David Wallace", "price": 95.0,
                           "year": "2014", "class_id": "POLI 1010", "edition":1,"type":"HC","condition":"NW","seller":"1"})
        self.assertAlmostEquals(response.status_code, 201)

    def testReadBook(self):
        c = Client()
        response = c.get("api/v1/books/(?P<book_id>\d+)", kwargs={'book_id': 1})
        self.assertAlmostEquals(response.status_code, 201)
        response2 = c.get("api/v1/books/(?P<book_id>\d+)", kwargs={'book_id': 3})
        self.assertAlmostEquals(response2.status_code, 404)

    def testUpdateBook(self):
        c = Client()
        response = c.post("api/v1/books/(?P<book_id>\d+)/update", {"price": 85.0}, kwargs={'book_id': 1})
        self.assertAlmostEquals(response.status_code, 201)

    def testDeleteBook(self):
        c = Client()
        response = c.post("api/v1/books/(?P<book_id>\d+)/delete", kwargs={'book_id': 1})
        self.assertAlmostEquals(response.status_code, 405)
        response2 = c.get("api/v1/books/(?P<book_id>\d+)/delete", kwargs={'book_id': 1})
        self.assertAlmostEquals(response2.status_code, 201)

    def tearDown(self):
        pass
