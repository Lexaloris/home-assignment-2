import os
import unittest
from selenium import webdriver
from pageObject import AuthPage
from helper import USERNAME, USEREMAIL, PASSWORD


class AuthTest(unittest.TestCase):

    def setUp(self):

        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        if browser == 'FIREFOX':
            self.driver = webdriver.Firefox()
        elif browser == 'CHROME':
            self.driver = webdriver.Chrome()

        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_form = auth_page.form
        auth_form.open_form()
        auth_form.set_login(USEREMAIL)
        auth_form.set_password(PASSWORD)
        auth_form.submit()        

    def test_create_topic_empty_blog(self):
        auth_page = AuthPage(self.driver)
        user_name = auth_page.top_menu.get_username()
        self.assertEqual(USERNAME, user_name)

    def tearDown(self):
        self.driver.quit()        
