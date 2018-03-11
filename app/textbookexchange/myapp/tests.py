from django.test import TestCase, Client
from myapp import models
from django.http import HttpRequest
import json

# Create your tests here.
def send(post_data, url):
    c = Client()
    response = c.post(url, post_data)
    json_obj = json.loads((response.content).decode("utf-8"))
    return json_obj

def get(url):
    c = Client()
    response = c.get(url)
    json_obj = json.loads((response.content).decode("utf-8"))
    return json_obj


class CreateUserTestCase(TestCase):
    def setUp(self):
        pass

    def test_successful_response(self):
        post_data = {}
        post_data['first_name'] = 'foo'
        post_data['last_name'] = 'bar'
        post_data['username'] ='baz'
        post_data['email'] ='email@gmail.com'
        post_data['password'] = 'secret'
        self.assertTrue((send(post_data, '/api/v1/users/create')["ok"]))

    def test_first_name_error(self):
        post_data = {}
        post_data['last_name'] = 'bar'
        post_data['username'] ='baz'
        post_data['email'] ='email@gmail.com'
        post_data['password'] = 'secret'
        self.assertTrue(
            (send(post_data, '/api/v1/users/create')["error"]) == "Required field first_name was not supplied")

    def test_last_name_error(self):
        post_data = {}
        post_data['first_name'] = 'foo'
        post_data['username'] ='baz'
        post_data['email'] ='email@gmail.com'
        post_data['password'] = 'secret'
        self.assertTrue(
            (send(post_data, '/api/v1/users/create')["error"]) == "Required field last_name was not supplied")

    def test_username_error(self):
        post_data = {}
        post_data['first_name'] = 'foo'
        post_data['last_name'] = 'bar'
        post_data['password'] = 'secret'
        post_data['email'] = 'email@gmail.com'
        self.assertTrue(
            (send(post_data, '/api/v1/users/create')["error"]) == "Required field username was not supplied")

    def test_password_error(self):
        post_data = {}
        post_data['first_name'] = 'foo'
        post_data['last_name'] = 'bar'
        post_data['username'] = 'baz'
        post_data['email'] = 'email@gmail.com'
        self.assertTrue(
            (send(post_data, '/api/v1/users/create')["error"]) == "Required field password was not supplied")

    def test_email_error(self):
        post_data = {}
        post_data['first_name'] = 'foo'
        post_data['last_name'] = 'bar'
        post_data['username'] = 'baz'
        post_data['password'] = 'secret'
        self.assertTrue(
            (send(post_data, '/api/v1/users/create')["error"]) == "Required field email was not supplied")

    def test_existing_email_error(self):
        post_data = {}
        post_data['first_name'] = 'foo'
        post_data['last_name'] = 'bar'
        post_data['username'] = 'baz'
        post_data['password'] = 'secret'
        post_data['email'] = 'email@gmail.com'
        response = send(post_data, '/api/v1/users/create')
        post_data2 = {}
        post_data2['first_name'] = 'oof'
        post_data2['last_name'] = 'rab'
        post_data2['username'] = 'zab'
        post_data2['password'] = 'terces'
        post_data2['email'] = 'email@gmail.com'
        self.assertFalse(send(post_data2, '/api/v1/users/create')["ok"])

    def tearDown(self):
        pass

class GetUserDetailsTestCase(TestCase):
    def setUp(self):
        pass

    def test_successful_get(self):
        post_data = {}
        post_data['first_name'] = 'taylor'
        post_data['last_name'] = 'swift'
        post_data['username'] ='tswizzle'
        post_data['email'] ='tswift@gmail.com'
        post_data['password'] = 'redrum'
        response = send(post_data, '/api/v1/users/create')
        gotten = get('/api/v1/users/4')
        self.assertTrue(gotten['ok'])

