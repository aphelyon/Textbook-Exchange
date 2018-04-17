from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.test import TestCase, Client
import unittest

class SeleniumTest(unittest.TestCase):
    fixtures = ['selenium/db.json', ]

    def setUp(self):
        self.driver = webdriver.Remote(
        command_executor='http://192.168.99.100:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://165.227.202.249:8000")
        self.assertIn("Textbook Exchange", driver.title)


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()