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


def post(url):
    c = Client()
    response = c.post(url)
    json_obj = json.loads(response.content.decode("utf-8"))
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
        response = (send(post_data, '/api/v1/users/create'))
        self.assertTrue(response["ok"])
        # Check if the created object can be retrieved from the db and has the right fields
        response2 = (get('/api/v1/users/' + str(response['results']['User']['pk'])))['results']
        self.assertEqual(response2['first_name'], 'foo')
        self.assertEqual(response2['last_name'], 'bar')
        self.assertEqual(response2['username'], 'baz')
        self.assertEqual(response2['email'], 'email@gmail.com')

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

    def test_existing_username_error(self):
        post_data = {}
        post_data['first_name'] = 'foo'
        post_data['last_name'] = 'bar'
        post_data['username'] = 'mhc6kp'
        post_data['password'] = 'secret'
        post_data['email'] = 'email@gmail.com'

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

    def test_unsuccessful_get(self):
        gottan = get('/api/v1/users/5')
        self.assertFalse(gottan['ok'])

    def tearDown(self):
        pass

class UpdateUserDeatilsTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_Update_info(self):
        gottan = get('/api/v1/users/1')
        post_data = {}
        post_data['first_name'] = 'foo'
        post_data['last_name'] = 'adsk'
        post_data['username'] = 'm121hc6kp'
        post_data['password'] = 'se132cret'
        post_data['email'] = 'email112@gmail.com'
        gottan2 = send(post_data, '/api/v1/users/1')
        self.assertFalse(gottan['results']['first_name'] == gottan2['results']['first_name'])
        self.assertFalse(gottan['results']['last_name'] == gottan2['results']['last_name'])
        self.assertFalse(gottan['results']['username'] == gottan2['results']['username'])
        self.assertFalse(gottan['results']['email'] == gottan2['results']['email'])


    def tearDown(self):
        pass


class DeleteUserTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_successful_delete(self):
        self.assertTrue(post('/api/v1/users/1/delete')['ok'])
        self.assertFalse(get('/api/v1/users/1')['ok'])

    def test_user_not_found(self):
        self.assertFalse(get('/api/v1/users/5')['ok'])
        self.assertFalse(post('/api/v1/users/5/delete')['ok'])

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
        response = (send(post_data, '/api/v1/professors/create'))
        self.assertTrue(response["ok"])
        # Check if the created object can be retrieved from the db and has the right fields
        response2 = (get('/api/v1/professors/' + str(response['results']['pk'])))['results']
        self.assertEqual(response2['name'], 'Tom')

    def test_successful_post_with_email(self):
        post_data = {}
        post_data['name'] = 'Tom Brady'
        post_data['email'] = 'email@tombrady.com'
        response = (send(post_data, '/api/v1/professors/create'))
        self.assertTrue(response["ok"])
        # Check if the created object can be retrieved from the db and has the right fields
        response2 = (get('/api/v1/professors/' + str(response['results']['pk'])))['results']
        self.assertEqual(response2['name'], 'Tom Brady')
        self.assertEqual(response2['email'], 'email@tombrady.com')

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

    def test_unsuccessful_get(self):
        gotten = get('/api/v1/professors/6')
        self.assertFalse(gotten['ok'])

    def tearDown(self):
        pass

class UpdateProfessorDeatilsTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_Update_info(self):
        gottan = get('/api/v1/professors/2')
        post_data = {}
        post_data['name'] = 'foo'
        post_data['email'] = 'email112@gmail.com'
        gottan2 = send(post_data, '/api/v1/professors/2')
        self.assertFalse(gottan['results']['name'] == gottan2['results']['name'])
        self.assertFalse(gottan['results']['email'] == gottan2['results']['email'])


    def tearDown(self):
        pass


class DeleteProfessorTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_successful_delete(self):
        self.assertTrue(post('/api/v1/professors/2/delete')['ok'])
        self.assertFalse(get('/api/v1/professors/2')['ok'])

    def test_professor_not_found(self):
        self.assertFalse(get('/api/v1/professors/4')['ok'])
        self.assertFalse(post('/api/v1/professors/4/delete')['ok'])

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
        response = (send(post_data, '/api/v1/courses/create'))
        self.assertTrue(response["ok"])
        # Check if the created object can be retrieved from the db and has the right fields
        response2 = (get('/api/v1/courses/' + str(response['results']['pk'])))['results']
        self.assertEqual(response2['identifier'], 'ISBN13')
        self.assertEqual(response2['department'], 'math')
        self.assertEqual(response2['name'], 'Math1310')

    def test_successful_post_with_prof(self):
        post_data = {}
        post_data['identifier'] = 'ISBN13'
        post_data['department'] = 'math'
        post_data['professor_key'] = 2
        post_data['name'] = 'Math1310'
        response = (send(post_data, '/api/v1/courses/create'))
        self.assertTrue(response["ok"])
        # Check if the created object can be retrieved from the db and has the right fields
        response2 = (get('/api/v1/courses/' + str(response['results']['pk'])))['results']
        self.assertEqual(response2['identifier'], 'ISBN13')
        self.assertEqual(response2['department'], 'math')
        self.assertEqual(response2['name'], 'Math1310')
        self.assertEqual(response2['professor']['pk'], '2')

    def test_wrong_prof(self):
        post_data = {}
        post_data['identifier'] = 'ISBN13'
        post_data['department'] = 'math'
        post_data['professor_key'] = 1321412
        post_data['name'] = 'Math1310'
        #self.assertRaises(models.Professor.DoesNotExist, send(post_data,'/api/v1/courses/create'))
        self.assertTrue(
            (send(post_data, '/api/v1/courses/create')["error"]) == "Requested Professor object does not exist")

    def test_no_id(self):
        post_data = {}
        post_data['department'] = 'math'
        post_data['professor_key'] = 2
        post_data['name'] = 'Math1310'
        # self.assertRaises(models.Professor.DoesNotExist, send(post_data,'/api/v1/courses/create'))
        self.assertTrue(
            (send(post_data, '/api/v1/courses/create')["error"]) == "Required field identifier was not supplied")

    def test_no_department(self):
        post_data = {}
        post_data['identifier'] = 'math'
        post_data['professor_key'] = 2
        post_data['name'] = 'Math1310'
        # self.assertRaises(models.Professor.DoesNotExist, send(post_data,'/api/v1/courses/create'))
        self.assertTrue(
            (send(post_data, '/api/v1/courses/create')["error"]) == "Required field department was not supplied")

    def test_no_name(self):
        post_data = {}
        post_data['identifier'] = '1230981'
        post_data['department'] = 'Math'
        post_data['professor_key'] = 2
        # self.assertRaises(models.Professor.DoesNotExist, send(post_data,'/api/v1/courses/create'))
        self.assertTrue(
            (send(post_data, '/api/v1/courses/create')["error"]) == "Required field name was not supplied")

    def tearDown(self):
        pass


class GetCourseTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]
    def setUp(self):
        pass

    def test_successful_get(self):
        gottin = get('/api/v1/courses/1')
        self.assertTrue(gottin['ok'])

    def test_unsuccessful_get(self):
        gottin = get('/api/v1/courses/3')
        self.assertFalse(gottin['ok'])

    def teardown(self):
        pass

class UpdateCourseDeatilsTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_Update_info(self):
        gottan = get('/api/v1/courses/1')
        post_data = {}
        post_data['identifier'] = 'foo'
        post_data['department'] = 'adsk'
        post_data['name'] = 'se132cret'
        gottan2 = send(post_data, '/api/v1/courses/1')
        self.assertFalse(gottan['results']['identifier'] == gottan2['results']['identifier'])
        self.assertFalse(gottan['results']['department'] == gottan2['results']['department'])
        self.assertFalse(gottan['results']['name'] == gottan2['results']['name'])

    def tearDown(self):
        pass



class DeleteCourseTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]
    def setUp(self):
        pass

    def test_successful_delete(self):
        self.assertTrue(post('/api/v1/courses/1/delete')['ok'])
        self.assertFalse(get('/api/v1/courses/1')['ok'])

    def test_user_not_found(self):
        self.assertFalse(get('/api/v1/courses/4')['ok'])
        self.assertFalse(post('/api/v1/courses/4/delete')['ok'])

    def tearDown(self):
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
        response = (send(post_data, '/api/v1/textbooks/create'))
        self.assertTrue(response["ok"])
        # Check if the created object can be retrieved from the db and has the right fields
        response2 = (get('/api/v1/textbooks/' + str(response['results']['pk'])))['results']
        self.assertEqual(response2['title'], 'A')
        self.assertEqual(response2['author'], 'B')
        self.assertEqual(response2['ISBN'], 'ISBN1310')
        self.assertEqual(response2['pub_date'], '1979-10-12')

    def test_successful_post_with_course(self):
        post_data = {}
        post_data['item_title'] = 'Hitchhikerguide'
        post_data['item_author'] = 'IDK'
        post_data['course_key'] = 1
        post_data['item_ISBN'] = 'ISBN1310'
        post_data['pub_date'] = '1979-10-12'
        response = (send(post_data, '/api/v1/textbooks/create'))
        self.assertTrue(response["ok"])
        # Check if the created object can be retrieved from the db and has the right fields
        response2 = (get('/api/v1/textbooks/' + str(response['results']['pk'])))['results']
        self.assertEqual(response2['title'], 'Hitchhikerguide')
        self.assertEqual(response2['author'], 'IDK')
        self.assertEqual(response2['ISBN'], 'ISBN1310')
        self.assertEqual(response2['pub_date'], '1979-10-12')
        self.assertEqual(response2['course']['pk'], "1")


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
        self.assertTrue(
            (send(post_data, '/api/v1/textbooks/create')["error"]) == "pub_date not in required format YYYY-MM-DD")

    def test_unsuccessful_post_with_no_pub_date(self):
        post_data = {}
        post_data['item_title'] = 'A'
        post_data['item_author'] = 'B'
        post_data['item_ISBN'] = 'ISBN1310'
        self.assertTrue(
            (send(post_data, '/api/v1/textbooks/create')["error"]) == "Required field pub_date was not supplied")

    def test_unsuccessful_post_with_no_title(self):
        post_data = {}
        post_data['item_author'] = 'Me'
        post_data['course_key'] = 1
        post_data['item_ISBN'] = 'ISBN111122310'
        post_data['pub_date'] = '1979-01-12'
        self.assertTrue(
            (send(post_data, '/api/v1/textbooks/create')["error"]) == "Required field item_title was not supplied")

    def test_unsuccessful_post_with_no_author(self):
        post_data = {}
        post_data['item_title'] = 'What if'
        post_data['course_key'] = 1
        post_data['item_ISBN'] = 'ISBN11112122310'
        post_data['pub_date'] = '1999-01-12'
        self.assertTrue(
            (send(post_data, '/api/v1/textbooks/create')["error"]) == "Required field item_author was not supplied")

    def test_unsuccessful_post_with_no_ISBN(self):
        post_data = {}
        post_data['item_title'] = 'What if'
        post_data['item_author'] = 'XKCD guy'
        post_data['course_key'] = 1
        post_data['pub_date'] = '2014-01-12'
        self.assertTrue(
            (send(post_data, '/api/v1/textbooks/create')["error"]) == "Required field item_ISBN was not supplied")

    def teardown(self):
        pass


class GetTextbookTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]
    def setUp(self):
        pass

    def test_get_successful_textbook(self):
        gotton = get('/api/v1/textbooks/1')
        self.assertTrue(gotton['ok'])

    def test_get_unsuccessful_textbook(self):
        gotton = get('/api/v1/textbooks/4')
        self.assertFalse(gotton['ok'])

    def tearDown(self):
        pass


class UpdateTestbookrDeatilsTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_Update_info(self):
        gottan = get('/api/v1/textbooks/1')
        post_data = {}
        post_data['item_title'] = 'foo'
        post_data['item_author'] = 'adsk'
        post_data['item_ISBN'] = '132'
        post_data['pub_date'] = '1789-12-09'
        gottan2 = send(post_data, '/api/v1/textbooks/1')
        self.assertFalse(gottan['results']['title'] == gottan2['results']['title'])
        self.assertFalse(gottan['results']['author'] == gottan2['results']['author'])
        self.assertFalse(gottan['results']['ISBN'] == gottan2['results']['ISBN'])
        self.assertFalse(gottan['results']['pub_date'] == gottan2['results']['pub_date'])


    def tearDown(self):
        pass


class DeleteTextbookTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]
    def setUp(self):
        pass

    def test_successful_delete(self):
        self.assertTrue(post('/api/v1/textbooks/1/delete')['ok'])
        self.assertFalse(get('/api/v1/textbooks/1')['ok'])

    def test_user_not_found(self):
        self.assertFalse(get('/api/v1/textbooks/5')['ok'])
        self.assertFalse(post('/api/v1/textbooks/5/delete')['ok'])

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
        post_data['user_key'] = 1
        post_data['condition'] = 'USED_GOOD'
        post_data['status'] = 'For Sale'
        response = (send(post_data, '/api/v1/listings/create'))
        self.assertTrue(response["ok"])
        # Check if the created object can be retrieved from the db and has the right fields
        response2 = (get('/api/v1/listings/' + str(response['results']['pk'])))['results']
        self.assertEqual(response2['item']['pk'], '1')
        self.assertEqual(response2['price_text'], '100.2')
        self.assertEqual(response2['actualprice'], 100.2)
        self.assertEqual(response2['user']['pk'], '1')
        self.assertEqual(response2['condition'], 'USED_GOOD')
        self.assertEqual(response2['status'], 'For Sale')

    def test_successful_list_with_default_condition(self):
        post_data = {}
        post_data['textbook_key'] = 1
        post_data['price'] = 145
        post_data['user_key'] = 2
        post_data['status'] = 'For Sale'
        response = (send(post_data, '/api/v1/listings/create'))
        self.assertTrue(response["ok"])
        # Check if the created object can be retrieved from the db and has the right fields
        response2 = (get('/api/v1/listings/' + str(response['results']['pk'])))['results']
        self.assertEqual(response2['item']['pk'], '1')
        self.assertEqual(response2['price_text'], '145')
        self.assertEqual(response2['actualprice'], 145)
        self.assertEqual(response2['user']['pk'], '2')
        self.assertEqual(response2['condition'], 'NEW')
        self.assertEqual(response2['status'], 'For Sale')

    def test_successful_list_with_default_status(self):
        post_data = {}
        post_data['textbook_key'] = 1
        post_data['price'] = 145
        post_data['user_key'] = 2
        post_data['condition'] = 'USED_GOOD'
        response = (send(post_data, '/api/v1/listings/create'))
        self.assertTrue(response["ok"])
        # Check if the created object can be retrieved from the db and has the right fields
        response2 = (get('/api/v1/listings/' + str(response['results']['pk'])))['results']
        self.assertEqual(response2['item']['pk'], '1')
        self.assertEqual(response2['price_text'], '145')
        self.assertEqual(response2['actualprice'], 145)
        self.assertEqual(response2['user']['pk'], '2')
        self.assertEqual(response2['condition'], 'USED_GOOD')
        self.assertEqual(response2['status'], 'For Sale')

    def test_unsuccessful_list_wrong_textbook_key(self):
        post_data = {}
        post_data['textbook_key'] = 5
        post_data['price'] = 100.2
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

    def test_unsuccessful_list_price_DNE(self):
        post_data = {}
        post_data['textbook_key'] = 1
        post_data['user_key'] = 1
        post_data['condition'] = 'NEW'
        post_data['status'] = 'For Sale'
        self.assertTrue(
            (send(post_data, '/api/v1/listings/create')["error"]) == "Required field price was not supplied")

    def test_unsuccessful_list_user_key_DNE(self):
        post_data = {}
        post_data['textbook_key'] = 1
        post_data['price'] = 100.2
        post_data['user_key'] = 5
        post_data['condition'] = 'NEW'
        post_data['status'] = 'For Sale'
        self.assertTrue(
            (send(post_data, '/api/v1/listings/create')["error"]) == "Requested User object does not exist")

    def test_unsuccessful_list_user_key_field_DNE(self):
        post_data = {}
        post_data['textbook_key'] = 1
        post_data['price'] = 100.2
        post_data['condition'] = 'NEW'
        post_data['status'] = 'For Sale'
        self.assertTrue(
            (send(post_data, '/api/v1/listings/create')["error"]) == "Required field user_key was not supplied")

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

    def test_get_unsuccessful_textbook(self):
        gottun = get('/api/v1/listings/5')
        self.assertFalse(gottun['ok'])

    def tearDown(self):
        pass

class UpdateListingDeatilsTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_Update_info(self):
        gottan = get('/api/v1/listings/1')
        post_data = {}
        post_data['textbook_key'] = 1
        post_data['price'] = 123.45
        post_data['condition'] = 'USED_POOR'
        post_data['status'] = 'Sold'
        gottan2 = send(post_data, '/api/v1/listings/1')
        self.assertFalse(gottan['results']['item']['pk'] == gottan2['results']['item']['pk'])
        self.assertFalse(gottan['results']['actualprice'] == gottan2['results']['actualprice'])
        self.assertFalse(gottan['results']['condition'] == gottan2['results']['condition'])
        self.assertFalse(gottan['results']['status'] == gottan2['results']['status'])


    def tearDown(self):
        pass


class DeleteListingTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_successful_delete(self):
        self.assertTrue(post('/api/v1/listings/1/delete')['ok'])
        self.assertFalse(get('/api/v1/listings/1')['ok'])

    def test_user_not_found(self):
        self.assertFalse(get('/api/v1/listings/4')['ok'])
        self.assertFalse(post('/api/v1/listings/4/delete')['ok'])
        self.assertEqual(post('/api/v1/listings/4/delete')['error'], "Requested Listing object does not exist")

    def tearDown(self):
        pass


class ViewCountTestCase(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_increment_listing_viewcount(self):
        self.assertTrue(get('/api/v1/listings/1/incrementCount')['ok'])
        self.assertEqual(get('/api/v1/listings/1')['results']['viewed_count'], 1)

    def test_failed_increment_listing(self):
        self.assertFalse(get('/api/v1/listings/5/incrementCount')['ok'])
        self.assertEqual(post('/api/v1/listings/5/incrementCount')['error'], "Requested Listing object does not exist")

    def test_increment_course_viewcount(self):
        self.assertTrue(get('/api/v1/courses/2/incrementCount')['ok'])
        self.assertEqual(get('/api/v1/courses/2')['results']['viewed_count'], 1)

    def test_failed_increment_course(self):
        self.assertFalse(get('/api/v1/courses/5/incrementCount')['ok'])
        self.assertEqual(post('/api/v1/courses/4/incrementCount')['error'], "Requested Course object does not exist")

    def tearDown(self):
        pass


class MostViewedTestCase(TestCase):
    fixtures = ['myapp/fixtures/dbWithMoreStuff.json', ]

    def setUp(self):
        pass

    def test_most_viewed_listings(self):
        jsonObject = get('/api/v1/listings/most_viewed')
        self.assertEqual(jsonObject['results'][0]['pk'], "5")
        self.assertEqual(jsonObject['results'][1]['pk'], "2")
        self.assertEqual(jsonObject['results'][2]['pk'], "3")
        self.assertEqual(jsonObject['results'][3]['pk'], "4")
        self.assertEqual(jsonObject['results'][4]['pk'], "6")
        self.assertEqual(len(jsonObject['results']), 5)

    def test_most_viewed_listings_less_than_five(self):
        post('/api/v1/listings/2/delete')
        post('/api/v1/listings/4/delete')
        post('/api/v1/listings/6/delete')
        jsonObject = get('/api/v1/listings/most_viewed')
        self.assertEqual(jsonObject['results'][0]['pk'], "5")
        self.assertEqual(jsonObject['results'][1]['pk'], "3")
        self.assertEqual(jsonObject['results'][2]['pk'], "1")
        self.assertEqual(len(jsonObject['results']), 3)

    def test_most_viewed_courses(self):
        jsonObject = get('/api/v1/courses/most_viewed')
        self.assertEqual(jsonObject['results'][0]['pk'], "1")
        self.assertEqual(jsonObject['results'][1]['pk'], "5")
        self.assertEqual(jsonObject['results'][2]['pk'], "4")
        self.assertEqual(jsonObject['results'][3]['pk'], "3")
        self.assertEqual(jsonObject['results'][4]['pk'], "2")
        self.assertEqual(len(jsonObject['results']), 5)

    def test_most_viewed_courses_less_than_five(self):
        post('/api/v1/courses/2/delete')
        post('/api/v1/courses/4/delete')
        post('/api/v1/courses/6/delete')
        jsonObject = get('/api/v1/courses/most_viewed')
        self.assertEqual(jsonObject['results'][0]['pk'], "1")
        self.assertEqual(jsonObject['results'][1]['pk'], "5")
        self.assertEqual(jsonObject['results'][2]['pk'], "3")
        self.assertEqual(len(jsonObject['results']), 3)

    def tearDown(self):
        pass


class NewListingsTestCase(TestCase):

    fixtures = ['myapp/fixtures/dbWithMoreStuff.json', ]

    def setUp(self):
        pass

    def test_newest_listings(self):
        jsonObject = get('/api/v1/listings/newest')
        self.assertEqual(jsonObject['results'][0]['pk'], "5")
        self.assertEqual(jsonObject['results'][1]['pk'], "1")
        self.assertEqual(jsonObject['results'][2]['pk'], "6")
        self.assertEqual(jsonObject['results'][3]['pk'], "2")
        self.assertEqual(jsonObject['results'][4]['pk'], "3")
        self.assertEqual(len(jsonObject['results']), 5)

    def test_newest_listings_less_than_five(self):
        post('/api/v1/listings/2/delete')
        post('/api/v1/listings/4/delete')
        post('/api/v1/listings/6/delete')
        jsonObject = get('/api/v1/listings/newest')
        self.assertEqual(jsonObject['results'][0]['pk'], "5")
        self.assertEqual(jsonObject['results'][1]['pk'], "1")
        self.assertEqual(jsonObject['results'][2]['pk'], "3")
        self.assertEqual(len(jsonObject['results']), 3)

    def tearDown(self):
        pass


class ReverseLookup(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_course_textbooks(self):
        jsonObjectTextbooks = get('/api/v1/textbooks/from_course/1')
        jsonObjectNoTextbooks = get('/api/v1/textbooks/from_course/2')
        jsonObjectCourseDoesNotExist = get('/api/v1/textbooks/from_course/3')
        self.assertTrue(jsonObjectTextbooks['ok'])
        self.assertEqual(jsonObjectTextbooks['results'][0]['pk'], "1")
        self.assertTrue(jsonObjectNoTextbooks['ok'])
        self.assertNotIn('results', jsonObjectNoTextbooks)
        self.assertFalse(jsonObjectCourseDoesNotExist['ok'])

    def test_textbook_listings(self):
        jsonObjectListings = get('/api/v1/listings/from_textbook/2')
        jsonObjectNoListings = get('/api/v1/listings/from_textbook/1')
        jsonObjectTextbookDoesNotExist = get('/api/v1/listings/from_textbook/3')
        self.assertTrue(jsonObjectListings['ok'])
        self.assertEqual(jsonObjectListings['results'][0]['pk'], "1")
        self.assertTrue(jsonObjectNoListings['ok'])
        self.assertNotIn('results', jsonObjectNoListings)
        self.assertFalse(jsonObjectTextbookDoesNotExist['ok'])

    def tearDown(self):
        pass


class Authenticator(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setUp(self):
        pass

    def test_authenticator(self):
        jsonObjectAuthenticator = send({'username': 'tmh6de', 'password': 'cool_password'}, '/api/v1/users/login')
        self.assertTrue(jsonObjectAuthenticator['ok'])
        self.assertEqual(jsonObjectAuthenticator['results']['authenticator']['user_id'], 4)
        jsonObjectCheck = send({'authenticator': jsonObjectAuthenticator['results']['authenticator']['authenticator']}, '/api/v1/authenticators/check')
        self.assertTrue(jsonObjectCheck['ok'])
        # Change authenticator to invalid value to check if an invalid authenticator fails
        jsonObjectAuthenticator['results']['authenticator']['authenticator'] = '12345'
        jsonObjectCheck2 = send({'authenticator': jsonObjectAuthenticator['results']['authenticator']['authenticator']}, '/api/v1/authenticators/check')
        self.assertFalse(jsonObjectCheck2['ok'])

    def test_delete_authenticator(self):
        jsonObjectAuthenticator = send({'username': 'tmh6de', 'password': 'cool_password'}, '/api/v1/users/login')
        self.assertTrue(jsonObjectAuthenticator['ok'])  # Just make sure the authenticator is returned fine
        jsonObjectDeleteResponse = send({'authenticator': jsonObjectAuthenticator['results']['authenticator']
                                        ['authenticator']}, '/api/v1/authenticators/delete')
        self.assertTrue((jsonObjectDeleteResponse['ok']))
        # If we send it again, we should get a "false" result, because the object is already gone
        jsonObjectDeleteResponse2 = send({'authenticator': jsonObjectAuthenticator['results']['authenticator']
                              ['authenticator']}, '/api/v1/authenticators/delete')
        self.assertFalse(jsonObjectDeleteResponse2['ok'])
        self.assertEqual(jsonObjectDeleteResponse2['error'], "Requested authenticator object does not exist")

    def tearDown(self):
        pass

class get_all(TestCase):
    fixtures = ['myapp/fixtures/db.json', ]

    def setYp(self):
        pass

    def test_get_all_textbooks(self):
        gottan = get('/api/v1/textbooks/get_all')
        self.assertTrue(gottan['ok'])
        post_data = {}
        post_data['item_title'] = 'Hitchhikerguide'
        post_data['item_author'] = 'IDK'
        post_data['course_key'] = 1
        post_data['item_ISBN'] = 'ISBN1310'
        post_data['pub_date'] = '1979-10-12'
        send(post_data, '/api/v1/textbooks/create')
        gotten = get(('/api/v1/textbooks/get_all'))
        self.assertNotEqual(gottan, gotten)

    def test_get_all_courses(self):
        gottan = get('/api/v1/courses/get_all')
        self.assertTrue(gottan['ok'])
        post_data = {}
        post_data['identifier'] = 'ISBN13'
        post_data['department'] = 'math'
        post_data['professor_key'] = 2
        post_data['name'] = 'Math1310'
        send(post_data, '/api/v1/courses/create')
        gotten = get(('/api/v1/courses/get_all'))
        self.assertNotEqual(gottan, gotten)

    def test_get_all_professors(self):
        gottan = get('/api/v1/professors/get_all')
        self.assertTrue(gottan['ok'])
        post_data = {}
        post_data['name'] = 'Tom'
        post_data['email'] = None
        send(post_data, '/api/v1/professors/create')
        gotten = get(('/api/v1/professors/get_all'))
        self.assertNotEqual(gottan, gotten)

    def tearDown(self):
        pass