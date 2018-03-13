from django.test import TestCase, Client
from .models import Book, Buyer, Seller, GenericUser
from django.core.urlresolvers import reverse


class TestBuyers(TestCase):

    def setUp(self):
        pass

    def testBuyer(self):
        c = Client()
        createResponse = c.post("/api/v1/buyers/create", {"name": "John Doe", "phone": "123456789", "email": "hello@gmail.com", "password": "pwd", "username": "JDoe", "address": "Earth", "rating": 9.0, "activity_score": 5.0})
        self.assertAlmostEquals(createResponse.status_code, 201)

        getResponseValid = c.get("/api/v1/buyers/1")
        self.assertAlmostEquals(getResponseValid.status_code, 200)

        getResponseInValid = c.get("/api/v1/buyers/3")
        self.assertAlmostEquals(getResponseInValid.status_code, 404)
        updateResponse = c.post("/api/v1/buyers/1/update", {"email": "newemail@yahoo.com"})
        self.assertAlmostEquals(updateResponse.status_code, 200)
        deleteResponseValid = c.get("/api/v1/buyers/1/delete")
        self.assertAlmostEquals(deleteResponseValid.status_code, 200)
        deleteResponseInValid = c.post("/api/v1/buyers/3/delete")
        self.assertAlmostEquals(deleteResponseInValid.status_code, 405)

    def tearDown(self):
        pass


class TestSellers(TestCase):

    def setUp(self):
        pass

    def testSeller(self):
        c = Client()
        createResponse = c.post("/api/v1/sellers/create", {"name": "John Doe", "phone": "123456789", "email": "hello@gmail.com", "password": "pwd", "username": "JDoe"})
        self.assertAlmostEquals(createResponse.status_code, 201)

        getResponseValid = c.get("/api/v1/sellers/2")
        self.assertAlmostEquals(getResponseValid.status_code, 200)

        getResponseInValid = c.get("/api/v1/sellers/3")
        self.assertAlmostEquals(getResponseInValid.status_code, 404)

        updateResponse = c.post("/api/v1/sellers/2/update", {"email": "newemail@yahoo.com"})
        self.assertAlmostEquals(updateResponse.status_code, 200)

        deleteResponseValid = c.get("api/v1/sellers/2/delete")
        self.assertAlmostEquals(deleteResponseValid.status_code, 200)


    def tearDown(self):
        pass


class TestBooks(TestCase):

    def setUp(self):
        pass

    def testBook(self):
        c = Client()
        response = c.post("/api/v1/sellers/create",
                          {"name": "Sarah Jane", "phone": "987654321", "email": "sjane@gmail.com", "password": "pass",
                           "username": "SJane", "rating": 7.5, "activity_score": 8.0})
        createResponse = c.post("/api/v1/books/create",
                          {"title": "Intro to Politics", "ISBN": "343459789", "author": "David Wallace", "price": 95.0,
                           "year": "2014", "class_id": "POLI 1010", "edition":1,"type":"HC","condition":"NW","seller":"1"})
        self.assertAlmostEquals(createResponse.status_code, 201)
        getResponseValid = c.get("/api/v1/books/1")
        self.assertAlmostEquals(getResponseValid.status_code, 200)
        getResponseInValid = c.get("/api/v1/books/3")
        self.assertAlmostEquals(getResponseInValid.status_code, 404)
        updateResponse = c.post("/api/v1/books/1/update", {"price": 85.0})
        self.assertAlmostEquals(updateResponse.status_code, 200)
        deleteResponseInValid = c.post("/api/v1/books/1/delete")
        self.assertAlmostEquals(deleteResponseInValid.status_code, 405)
        deleteResponseValid = c.get("/api/v1/books/1/delete")
        self.assertAlmostEquals(deleteResponseValid.status_code, 200)





    def tearDown(self):
        pass
