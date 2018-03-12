from django.test import TestCase, Client
from .models import Book, Buyer, Seller, GenericUser
from django.core.urlresolvers import reverse

class TestBuyers(TestCase):

    def setUp(self):

        self.buyer = Buyer.objects.create_buyer(name="John Doe", phone= "123456789", email= "hello@gmail.com", password = "pwd", username = "JDoe", address = "Earth", rating = 9.0, activity_score=5.0);
# Create your tests here.
        self.buyer.save()

    def testCreate(self):
        #self.assertEqual(self.buyer.address, "Earth")
        response = self.client.post(reverse("create_buyer", kwargs={'buyer_id':1}))
        self.assertAlmostEquals(response.status_code, 200)

    def testRead(self):
        pass
    #def testUpdate(self):

    #def testDelete(self):

    #def tearDown(self):
        #pass
