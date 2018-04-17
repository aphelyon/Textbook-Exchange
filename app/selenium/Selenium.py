from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


driver = webdriver.Remote(
   command_executor='http://192.168.99.100:4444/wd/hub',
   desired_capabilities=DesiredCapabilities.CHROME)
#driver = webdriver.Chrome()
driver.get("http://165.227.202.249:8000")
if not "Textbook Exchange" in driver.title:
    raise Exception("Unable to load page!")
if "Textbook Exchange" in driver.title:
    print("yeahyeah")

