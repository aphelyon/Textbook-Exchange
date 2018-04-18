from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from django.test import TestCase, Client
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import unittest

#Some code taken from the Selenium python documentation
class SeleniumTest(unittest.TestCase):
    fixtures = ['selenium/db.json', ]

    def setUp(self):
        self.driver = webdriver.Remote(
        command_executor='http://selenium-chrome:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)

    def test_search_in_python_org(self):
        driver = self.driver
        #gets the digital ocean homepage for our project
        driver.get("http://165.227.202.249:8000")
        print(driver.title)
        #check if the get is successful
        self.assertIn("Textbook Exchange", driver.title)
        #get the login page
        driver.get("http://165.227.202.249:8000/login")
        cookies = driver.get_cookies()
        login_status = False
        for cookie in cookies:
            if cookie['name'] == 'auth':
                login_status = True
                break
        #make sure that the login cookies named auth does not already exist
        self.assertFalse(login_status)
        #perform login
        usernameElement = driver.find_element_by_name("username")
        passwordElement = driver.find_element_by_name("password")
        usernameElement.send_keys("tmh6de")
        passwordElement.send_keys("cool_password")
        passwordElement.send_keys(Keys.ENTER)
        driver.implicitly_wait(5)
        cookies = driver.get_cookies()  # returns list of dicts
        login_status2 = False
        for cookie in cookies:
            if cookie['name'] == 'auth':
                login_status2 = True
                break
        #if auth cookie exist, then that means login is successful.
        self.assertTrue(login_status2)
        #go to listing page, if not logged in it should go back to login page
        driver.get("http://165.227.202.249:8000/listing")
        #create listing
        priceElement = driver.find_element_by_name("price")
        priceElement.send_keys("239")
        priceElement.send_keys(Keys.ENTER)
        driver.implicitly_wait(5)
        create_test = False
        #This checks whether the create listing operation is successful
        #Also, the if statement actually doesn't serve much purpose because
        #an error would occur if the driver.find... finds nothing. So if error doesn't then it is good.
        if driver.find_element_by_link_text("tmh6de") is not None:
            create_test = True
        self.assertTrue(create_test)
        #Below checks whether search function works
        search = driver.find_element_by_name('search')
        search.send_keys("Hitchikers Guide to the Galaxy")
        search.send_keys(Keys.ENTER)
        search_test = True
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Hitchikers Guide to the Galaxy ($239)')))
        print(element)
        if driver.find_element_by_link_text("Hitchikers Guide to the Galaxy ($239)") == element:
            search_test = True
        self.assertTrue(search_test)
        #Below checks if create professor works
        driver.get('http://165.227.202.249:8000/professor')
        name = driver.find_element_by_name("name")
        email = driver.find_element_by_name('email')
        name.send_keys('myprof')
        email.send_keys('myemail@email.com')
        email.send_keys(Keys.ENTER)
        driver.implicitly_wait(3)
        create_prof = False
        if driver.find_element_by_link_text("Create a Course with your new professor.") is not None:
            create_prof = True
        self.assertTrue(create_prof)
        #Below checks if you can create a course
        driver.get('http://165.227.202.249:8000/course')
        name2 = driver.find_element_by_name("name")
        identifier = driver.find_element_by_name("identifier")
        department = driver.find_element_by_name("department")
        name2.send_keys("cool_course")
        identifier.send_keys("1234")
        department.send_keys("math")
        department.send_keys(Keys.ENTER)
        driver.implicitly_wait(5)
        create_course = False
        if driver.find_element_by_link_text("tp3ks@virginia.edu") is not None:
            create_course = True
        self.assertTrue(create_course)
        # Below check if you can create a textbook
        driver.get('http://165.227.202.249:8000/textbook')
        title = driver.find_element_by_name('title')
        author = driver.find_element_by_name('author')
        ISBN = driver.find_element_by_name('isbn')
        pubdate = driver.find_element_by_name('pub_date')
        title.send_keys('cool_book')
        author.send_keys('cool author')
        ISBN.send_keys('9781234560')
        pubdate.send_keys('2012-01-02')
        pubdate.send_keys(Keys.ENTER)
        driver.implicitly_wait(5)
        create_textbook = False
        if driver.find_element_by_link_text("CS 2150") is not None:
            create_textbook = True
        self.assertTrue(create_textbook)
        
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

