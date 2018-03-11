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
    fixtures = ['myapp/fixtures/db.json',]
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
    fixtures = ['myapp/fixtures/db.json', ]
    def setUp(self):
        pass

    def test_successful_get(self):
        gottan = get('/api/v1/users/1')
        self.assertTrue(gottan['ok'])

    def tearDown(self):
        pass

class CreateProfTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]
    def setUp(self):
        pass

    def test_successful_post(self):
        post_data = {}
        post_data['name'] = 'Tom'
        post_data['email'] = None
        self.assertTrue((send(post_data, '/api/v1/professors/create')["ok"]))

    def test_successful_post_with_email(self):
        post_data = {}
        post_data['name'] = 'Tom Brady'
        post_data['email'] = 'email@tombrady.com'
        self.assertTrue((send(post_data, '/api/v1/professors/create')["ok"]))

    def test_bad_name(self):
        post_data = {}
        post_data['email'] = 'asdas'
        self.assertTrue(
            (send(post_data, '/api/v1/professors/create')["error"]) == "Required field name was not supplied")

    def tearDown(self):
        pass

class GetProfdetailtestcase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]
    def setUp(self):
        pass
    def test_successful_get(self):
        gotten = get('/api/v1/professors/3')
        self.assertTrue(gotten['ok'])
    def tearDown(self):
        pass

class CreateCourseTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]
    def setUp(self):
        pass

    def test_successful_post_without_prof(self):
        post_data = {}
        post_data['identifier'] = 'ISBN13'
        post_data['department'] = 'math'
        post_data['name'] = 'Math1310'
        self.assertTrue((send(post_data, '/api/v1/courses/create')["ok"]))

    def test_successful_post_with_prof(self):
        post_data = {}
        post_data['identifier'] = 'ISBN13'
        post_data['department'] = 'math'
        post_data['professor_key'] = 2
        post_data['name'] = 'Math1310'
        self.assertTrue((send(post_data, '/api/v1/courses/create')["ok"]))

    def test_wrong_prof(self):
        post_data = {}
        post_data['identifier'] = 'ISBN13'
        post_data['department'] = 'math'
        post_data['professor_key'] = 128391028
        post_data['name'] = 'Math1310'
        #self.assertRaises(models.Professor.DoesNotExist, send(post_data,'/api/v1/courses/create'))
        self.assertTrue(
            (send(post_data, '/api/v1/courses/create')["error"]) == "Requested Professor object does not exist")

    def tearDown(self):
        pass

class GetCourseTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]
    def setUp(self):
        pass

    def test_successful_get(self):
        gottin = get('/api/v1/courses/1')
        self.assertTrue(gottin['ok'])

    def teardown(self):
        pass

class CreateTextbookTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]
    def setUp(self):
        pass

    def test_successful_post_without_course(self):
        post_data = {}
        post_data['item_title'] = 'A'
        post_data['item_author'] = 'B'
        post_data['item_ISBN'] = 'ISBN1310'
        post_data['pub_date'] = '1979-10-12'
        self.assertTrue((send(post_data, '/api/v1/textbooks/create')["ok"]))

    def test_successful_post_with_course(self):
        post_data = {}
        post_data['item_title'] = 'Hitchhikerguide'
        post_data['item_author'] = 'IDK'
        post_data['course_key'] = 1
        post_data['item_ISBN'] = 'ISBN1310'
        post_data['pub_date'] = '1979-10-12'
        self.assertTrue((send(post_data, '/api/v1/textbooks/create')["ok"]))

    def test_unsuccessful_post_with_wrong_course(self):
        post_data = {}
        post_data['item_title'] = 'My cool box'
        post_data['item_author'] = 'Me'
        post_data['course_key'] = 42
        post_data['item_ISBN'] = 'ISBN1112310'
        post_data['pub_date'] = '1979-11-12'
        self.assertTrue(
            (send(post_data, '/api/v1/textbooks/create')["error"]) == "Requested Course object does not exist")

    def test_unsuccessful_post_with_wrong_pub_date(self):
        post_data = {}
        post_data['item_title'] = 'A'
        post_data['item_author'] = 'B'
        post_data['item_ISBN'] = 'ISBN1310'
        post_data['pub_date'] = 12/21/1221
        #self.assertTrue((send(post_data, '/api/v1/textbooks/create')["ok"]))
        self.assertTrue(
            (send(post_data, '/api/v1/textbooks/create')["error"]) == "pub_date not in required format YYYY-MM-DD")

    def teardown(self):
        pass

class GetTextbookTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]
    def setUp(self):
        pass

    def test_get_successful_textbook(self):
        gotton = get('/api/v1/textbooks/1')
        self.assertTrue(gotton['ok'])

    def tearDown(self):
        pass

class CreatelistingTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_successful_list(self):
        post_data = {}
        post_data['textbook_key'] = 1
        post_data['price'] = 100.2
        #post_data['actualprice'] = 100.2
        post_data['user_key'] = 1
        post_data['condition'] = 'NEW'
        post_data['status'] = 'For Sale'
        self.assertTrue((send(post_data, '/api/v1/listings/create')["ok"]))

    def test_unsuccessful_list_wrong_textbook_key(self):
        post_data = {}
        post_data['textbook_key'] = 5
        post_data['price'] = 100.2
        # post_data['actualprice'] = 100.2
        post_data['user_key'] = 1
        post_data['condition'] = 'NEW'
        post_data['status'] = 'For Sale'
        self.assertTrue(
            (send(post_data, '/api/v1/listings/create')["error"]) == "Requested Textbook object does not exist")

    def test_unsuccessful_list_no_textbook_key(self):
        post_data = {}
        post_data['price'] = 100.2
        # post_data['actualprice'] = 100.2
        post_data['user_key'] = 1
        post_data['condition'] = 'NEW'
        post_data['status'] = 'For Sale'
        self.assertTrue(
            (send(post_data, '/api/v1/listings/create')["error"]) == "Required field textbook_key was not supplied")

    def test_unsuccessful_list_price_cannot_convert(self):
        post_data = {}
        post_data['textbook_key'] = 1
        post_data['price'] = 'abc'
        # post_data['actualprice'] = 100.2
        post_data['user_key'] = 1
        post_data['condition'] = 'NEW'
        post_data['status'] = 'For Sale'
        self.assertTrue(
            (send(post_data, '/api/v1/listings/create')["error"]) == "Price cannot be converted to a float")

    def test_unsuccessful_list_user_key_DNE(self):
        post_data = {}
        post_data['textbook_key'] = 1
        post_data['price'] = 100.2
        # post_data['actualprice'] = 100.2
        post_data['user_key'] = 4
        post_data['condition'] = 'NEW'
        post_data['status'] = 'For Sale'
        self.assertTrue(
            (send(post_data, '/api/v1/listings/create')["error"]) == "Requested User object does not exist")

    def test_unsuccessful_list_condition_wrong(self):
        post_data = {}
        post_data['textbook_key'] = 1
        post_data['price'] = 100.2
        # post_data['actualprice'] = 100.2
        post_data['user_key'] = 1
        post_data['condition'] = 'old'
        post_data['status'] = 'For Sale'
        cond = "Condition provided is not in list: " + str(models.Listing.condition_of_textbook)
        self.assertTrue(
            (send(post_data, '/api/v1/listings/create')["error"]) == cond )

    def test_unsuccessful_list_status_wrong(self):
        post_data = {}
        post_data['textbook_key'] = 1
        post_data['price'] = 100.2
        # post_data['actualprice'] = 100.2
        post_data['user_key'] = 1
        post_data['condition'] = 'NEW'
        post_data['status'] = 'notforsale'
        stat = "Status provided is not in list: " + str(models.Listing.status_of_listing)
        self.assertTrue(
            (send(post_data, '/api/v1/listings/create')["error"]) == stat)

    def tearDown(self):
        pass

class GetListingTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_get_successful_textbook(self):
        gottun = get('/api/v1/listings/1')
        self.assertTrue(gottun['ok'])

    def tearDown(self):
        pass