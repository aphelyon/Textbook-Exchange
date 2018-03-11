from django.test import TestCase, Client
from myapp import models
from django.http import HttpRequest
import json

# Create your tests here.

class CreateUserTestCase(TestCase):
    def setUp(self):
        pass

    def test_successful_response(self):
        headerInfo = {'content-type': 'application/json'}
        post_data = {}
        post_data['first_name'] = 'foo'
        post_data['last_name'] = 'bar'
        post_data['username'] ='baz'
        post_data['email'] ='email@gmail.com'
        post_data['password'] = 'secret'
        c = Client()
        response = c.post('/api/v1/users/create', post_data)
        json_obj = json.loads((response.content).decode("utf-8"))
        self.assertEquals(json_obj["ok"], True)