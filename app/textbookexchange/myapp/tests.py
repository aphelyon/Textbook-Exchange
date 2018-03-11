from django.test import TestCase, Client
from myapp import models
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
        c = Client()
        response = c.post('/api/v1/users/create', headers=headerInfo, data = json.dumps(post_data))
        print(response.content)
        self.assertEquals(response["status"], "200")