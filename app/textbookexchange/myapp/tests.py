from django.test import TestCase
from myapp import models
import json

# Create your tests here.

class CreateUserTestCase(TestCase):
    def setUp(self):
        pass

    def test_successful_response(self):
        post_data = {'first_name': 'foo', 'last_name': 'bar', 'username': 'baz', 'email': 'email@gmail.com'}
        c = Client()
        response = c.post('v1/users/create', post_data)
        json_obj = json.loads((response.content).decode("utf-8"))
        self.assertEquals(json_obj["status"], "200")