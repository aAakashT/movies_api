import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import json
# Create your tests here.

class CollectionTesting(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpassword')
        token = RefreshToken.for_user(user=self.user)
        self.access_token = str(token.access_token)

    def test_create_collection(self):
        url = reverse('collection')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        data = {
            "title": "Test Collection",
            "description": "This is a test collection",
            "movies": [
                {
                    "title": "Test Movie",
                    "description": "This is a test movie",
                    "genres": "Action,Adventure",
                    "uuid": 1212121212121212
                },
                {
                    "title": "Test Movie 2",
                    "description": "This is a test movie 2",
                    "genres": "Action,Adventure",
                    "uuid": 1212121212343443
                }
            ],
            "uuid": 121212121234344454,
            "user": self.user.id
        }    
        response= self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        simple_data = json.loads(response.content)
        self.assertEqual(simple_data.get('collection_uuid'), data.get('uuid'))
        
    def test_get_collection(self):
        url =  reverse('collection')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    
    
    def test_request_count(self):
        url = reverse('count')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_reset_request_counter(self):
        url = reverse('CountResetView')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)     
    
    def tearDown(self) :
        res = self.user.delete()
        
if __name__ == "__main__":
    unittest.main()    
