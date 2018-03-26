from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class TestUsers(TestCase):

    def setUp(self):
        pass

    def testBuyer(self):
        c = Client()
        createResponse = c.post("/api/v1/users/create", {"name": "John Doe", "phone": "123456789", "email": "hello@gmail.com", "password": "pwd", "username": "JDoe", "address": "Earth", "rating": 9.0, "activity_score": 5.0})
        self.assertEquals(createResponse.status_code, 201)

        getResponseValid = c.get("/api/v1/users/1")
        self.assertEquals(getResponseValid.status_code, 200)

        getResponseValid = c.get("/api/v1/users/?username=danny")
        self.assertEquals(getResponseValid.status_code, 200)
        updateResponse = c.post("/api/v1/users/1/update", {"email": "newemail@yahoo.com"})
        self.assertEquals(updateResponse.status_code, 200)
        deleteResponseValid = c.get("/api/v1/users/1/delete")
        self.assertEquals(deleteResponseValid.status_code, 200)
        deleteResponseInValid = c.post("/api/v1/users/3/delete")
        self.assertEquals(deleteResponseInValid.status_code, 405)

    def tearDown(self):
        pass



class TestBooks(TestCase):

    def setUp(self):
        pass

    def testBook(self):
        c = Client()
        response = c.post("/api/v1/users/create",
                          {"name": "Sarah Jane", "phone": "987654321", "email": "sjane@gmail.com", "password": "pass",
                           "username": "SJane",})
        createResponse = c.post("/api/v1/books/create",
                          {"title": "Intro to Politics", "ISBN": "343459789", "author": "David Wallace", "price": 95.0,
                           "year": "2014", "class_id": "POLI 1010", "edition":1,"type":"HC","condition":"NW","seller":"1"})
        self.assertEquals(createResponse.status_code, 201)
        getResponseValid = c.get("/api/v1/books/1")
        self.assertEquals(getResponseValid.status_code, 200)
        getResponseInValid = c.get("/api/v1/books/?ISBN=1256897")
        self.assertEquals(getResponseInValid.status_code, 404)
        updateResponse = c.post("/api/v1/books/1/update", {"price": 85.0})
        self.assertEquals(updateResponse.status_code, 200)
        deleteResponseInValid = c.post("/api/v1/books/1/delete")
        self.assertEquals(deleteResponseInValid.status_code, 405)
        deleteResponseValid = c.get("/api/v1/books/1/delete")
        self.assertEquals(deleteResponseValid.status_code, 200)



    def tearDown(self):
        pass

class TestAuthentication(TestCase):

    def setUp(self):
        pass

    def testAuthentication(self):
        c = Client()

        loginResponse = c.post("/api/v1/login", {"username": "danny", "password": "Password2"})

        self.assertEquals(loginResponse.status_code, 200)



    def tearDown(self):
        pass