# -*- coding: utf-8 -*-

import time
import unittest
import os

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote

from pageObject import AuthPage, CreatePage
from helper import USERNAME, USEREMAIL, PASSWORD, BLOG, TITLE, TEXT


class NoneCreateTopicTest(unittest.TestCase):

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

        user_name = auth_page.top_menu.get_username()
        self.assertEqual(USERNAME, user_name)

        create_page = CreatePage(self.driver)
        create_page.open()
        self.create_form = create_page.form

    def tearDown(self):
        self.driver.quit()

    def test_create_topic_empty_blog(self):
        self.create_form.set_all_fields("", TITLE, TEXT)
        self.create_form.submit()
        self.assertTrue(self.create_form.is_message_error())

    def test_create_topic_empty_title(self):
        self.create_form.set_all_fields(BLOG, "", TEXT)
        self.create_form.submit()
        self.assertTrue(self.create_form.is_message_error())

    def test_create_topic_empty_text(self):
        self.create_form.set_all_fields(BLOG, TITLE, "")
        self.create_form.submit()
        self.assertTrue(self.create_form.is_message_error())

    def test_preview_text(self):
        self.create_form.set_all_fields(BLOG, TITLE, TEXT)
        self.create_form.preview.open()
        self.assertEqual(TEXT, self.create_form.preview.get_preview_text())
        self.create_form.submit()

    def test_create_topic_text_visiable(self):
        self.create_form.set_all_fields(BLOG, TITLE, TEXT)
        self.assertEqual(TEXT, self.create_form.get_text())

