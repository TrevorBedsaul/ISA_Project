from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import json


class TestUsers(TestCase):

    def setUp(self):
        pass

    def testUser(self):
        c = Client()
        createResponse = c.post("/api/v1/users/create", {"name": "JohnDoe", "phone": "123456789", "email": "hello@gmail.com", "password": "pwd", "username": "JDoe", "address": "Earth", "rating": 9.0, "activity_score": 5.0})
        self.assertEquals(createResponse.status_code, 201)
        user = json.loads(createResponse.content.decode("utf-8"))
        id = str(user["id"])

        getResponseValid = c.get("/api/v1/users?phone=123456789")
        self.assertEquals(getResponseValid.status_code, 200)

        getResponseValid = c.get("/api/v1/users?username=JDoe")
        self.assertEquals(getResponseValid.status_code, 200)
        updateResponse = c.post("/api/v1/users/"+id+"/update", {"email": "newemail@yahoo.com"})
        self.assertEquals(updateResponse.status_code, 200)
        deleteResponseValid = c.get("/api/v1/users/"+id+"/delete")
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
        user = json.loads(response.content.decode("utf-8"))
        id = str(user["id"])

        createResponse = c.post("/api/v1/books/create",
                          {"title": "Intro to Politics", "ISBN": "343459789", "author": "David Wallace", "price": 95.0,
                           "year": "2014", "class_id": "POLI 1010", "edition":1,"type_name":"HC","condition":"NW","seller":int(id)})
        self.assertEquals(createResponse.status_code, 201)
        getResponseEmpty = c.get("/api/v1/books?ISBN=1256897")
        empty_response = json.loads(getResponseEmpty.content.decode("utf-8"))
        self.assertEquals(len(empty_response), 0)
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

        response = c.post("/api/v1/users/create",
                          {"name": "Sarah Jane", "phone": "987654321", "email": "sjane@gmail.com", "password": "pass",
                           "username": "SJane",})

        loginResponse = c.post("/api/v1/login", {"username": "SJane", "password": "pass",})

        self.assertEquals(loginResponse.status_code, 200)
        login_json = json.loads(loginResponse.content.decode("utf-8"))
        newAuth = login_json["authenticator"]

        authenticatorResponse = c.post("/api/v1/check_authenticator", {"authenticator": newAuth})
        self.assertEquals(authenticatorResponse.status_code, 200)

        logoutResponse = c.post("/api/v1/logout", {"authenticator": newAuth})
        self.assertEquals(logoutResponse.status_code, 200)

    def tearDown(self):
        pass