# -*- coding: utf-8 -*-

import time
import unittest
import os

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote
from pageObject import AuthPage, CreatePage, TopicPage, BlogPage, Component, AuthForm, TopMenu, CreateForm, Topic, \
    EditForm
from helper import USERNAME, USEREMAIL, PASSWORD, BLOG, TITLE, TEXT, SUCCESS_NOTICE
from helper import LINK, NAME_OF_LINK, LINK_USER_NAME, LINK_USER_PROFILE, COMMENT
from helper import SUCCESS_EDITED_NOTICE, IMAGE_TITLE, LEFT, RIGHT, CENTER, URL_IMAGE, URL_ON_FTEST, IMAGE_LOCAL_PATH


class DeleteTopicTest(unittest.TestCase):

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
    
    def additional_assert(self, tag):
        topic_page = TopicPage(self.driver)
        self.assertEqual(TEXT, topic_page.topic.get_text(tag))            

    def tearDown(self):        
        blog_page = BlogPage(self.driver)
        blog_page.topic.delete()
        self.driver.quit()

    def test_create_topic_ok_after_create(self):
        self.create_form.set_all_fields(BLOG, TITLE, TEXT)
        self.create_form.submit()

        topic_page = TopicPage(self.driver)
        self.assertEqual(TITLE, topic_page.topic.get_title())
        self.assertEqual(BLOG.decode('utf-8'), topic_page.topic.get_blog())
        self.assertEqual(TEXT, topic_page.topic.get_text())
        self.assertEqual(USERNAME, topic_page.topic.get_username())
        self.assertEqual(u'0', topic_page.topic.get_favourite())
        self.assertEqual(u'0', topic_page.topic.get_comments_count())
        self.assertEqual(SUCCESS_NOTICE, topic_page.topic.get_notice())

    def test_create_topic_ok_open_blog(self):
        self.create_form.set_all_fields(BLOG, TITLE, TEXT)
        self.create_form.submit()

        topic_page = TopicPage(self.driver)
        topic_page.topic.open_blog()
        blog_page = BlogPage(self.driver)
        self.assertEqual(TITLE, blog_page.topic.get_title())
        self.assertEqual(BLOG.decode('utf-8'), topic_page.topic.get_blog())
        self.assertEqual(TEXT, blog_page.topic.get_text())
        self.assertEqual(USERNAME, blog_page.topic.get_username())
        self.assertEqual(u'0', topic_page.topic.get_favourite())
        self.assertEqual(u'0', topic_page.topic.get_comments_count())

    def test_editing_title_after_topic_create(self):
        self.create_form.set_all_fields(BLOG, TITLE, TEXT)
        self.create_form.submit()
        topic_page = TopicPage(self.driver)
        topic_page.topic.select_edit_topic()
        edit_form = EditForm(self.driver)
        edit_form.set_title(u'HоВыЙ')
        edit_form.store()
        self.assertEqual(TITLE+u'HоВыЙ', topic_page.topic.get_title())

    def test_editing_text_after_topic_create(self):
        self.create_form.set_all_fields(BLOG, TITLE, TEXT)
        self.create_form.submit()
        topic_page = TopicPage(self.driver)
        topic_page.topic.select_edit_topic()
        edit_form = EditForm(self.driver)
        edit_form.set_text_not_clicked(u'HоВыЙ')
        edit_form.store()
        self.assertEqual(TEXT+u'HоВыЙ', topic_page.topic.get_text())
        self.assertEqual(SUCCESS_EDITED_NOTICE, topic_page.topic.get_notice())

    def test_publish_from_preview(self):
        self.create_form.set_all_fields(BLOG, TITLE, TEXT)
        self.create_form.preview.open()
        self.create_form.preview.select_publish_topic()
        topic_page = TopicPage(self.driver)
        self.assertEqual(TEXT, topic_page.topic.get_text())

    def test_simple_comment_after_topic_create(self):
        self.create_form.set_all_fields(BLOG, TITLE, TEXT)
        self.create_form.submit()
        topic_page = TopicPage(self.driver)
        topic_page.comment.select_post_comment()
        topic_page.comment.set_comment(COMMENT)
        topic_page.comment.submit_comment()
        self.assertEqual(COMMENT, topic_page.topic.get_comments())

    def test_disallow_comments(self):
        self.create_form.set_all_fields(BLOG, TITLE, TEXT)
        self.create_form.select_disallow_comment()
        self.create_form.submit()
        topic_page = TopicPage(self.driver)
        self.assertFalse(topic_page.comment.select_post_comment())

    def test_create_draft(self):
        self.create_form.set_all_fields(BLOG, TITLE, TEXT)
        self.create_form.select_draft()
        self.create_form.submit()
        topic_page = TopicPage(self.driver)
        self.assertTrue(topic_page.topic.is_draft_icon_displayed())

    def test_create_topic_h4(self):
        tag = "/h4"
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_h4()
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_h5(self):
        tag = "/h5"
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_h5()
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_h6(self):
        tag = "/h6"
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_h6()
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_strong(self):
        tag = "/strong"
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_strong()
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_strong_with_ctrl_b(self):
        tag = "/strong"
        key = 'b'
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_ctrl_key(key)
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_em(self):
        tag = "/em"
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_em()
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_em_with_ctrl_i(self):
        tag = "/em"
        key = 'i'
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_ctrl_key(key)
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_s(self):
        tag = "/s"
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_s()
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_s_with_ctrl_s(self):
        tag = "/s"
        key = 's'
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_ctrl_key(key)
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_u(self):
        tag = "/u"
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_u()
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_u_with_ctrl_u(self):
        tag = "/u"
        key = 'u'
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_ctrl_key(key)
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_blockquote(self):
        tag = "/blockquote"
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_blockquote()
        self.create_form.steps_left(len(tag)+2)
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_code(self):
        tag = "/code"
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_code()
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_list_ul(self):
        tag = "/ul/li"
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_list_ul()
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_list_ol(self):
        tag = "/ol/li"
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_list_ol()
        self.create_form.set_text_clicked(TEXT)
        self.create_form.submit()
        self.additional_assert(tag)

    def test_create_topic_img_pc(self):
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_image()
        self.create_form.toolbar.image_form.select_pc()
        self.create_form.toolbar.image_form.set_image_path_pc(IMAGE_LOCAL_PATH)
        self.create_form.toolbar.image_form.submit_image_upload()
        self.create_form.submit()

        topic_page = TopicPage(self.driver)
        atr = "src"
        self.assertIsNotNone(topic_page.topic.get_image_atr(atr))

    def test_create_topic_img_url_upload_link(self):

        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_image()
        self.create_form.toolbar.image_form.select_link()
        self.create_form.toolbar.image_form.set_image_path_url(URL_IMAGE)
        self.create_form.toolbar.image_form.submit_image_upload_link()
        self.create_form.submit()

        topic_page = TopicPage(self.driver)
        self.assertEqual(u'http://'+URL_IMAGE, topic_page.topic.get_image_atr("src"))

    def test_create_topic_img_url_upload_link_upload(self):
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_image()
        self.create_form.toolbar.image_form.select_link()
        self.create_form.toolbar.image_form.set_image_path_url(URL_IMAGE)
        self.create_form.toolbar.image_form.submit_image_upload_link_upload()
        self.create_form.submit()

        topic_page = TopicPage(self.driver)
        self.assertTrue(URL_ON_FTEST in topic_page.topic.get_image_atr("src"))

    def test_create_topic_img_url_with_title(self):
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_image()
        self.create_form.toolbar.image_form.select_link()
        self.create_form.toolbar.image_form.set_image_path_url(URL_IMAGE)
        self.create_form.toolbar.image_form.set_image_url_title(IMAGE_TITLE)
        self.create_form.toolbar.image_form.submit_image_upload_link()
        self.create_form.submit()

        topic_page = TopicPage(self.driver)
        self.assertIsNotNone(topic_page.topic.get_image_atr("src"))
        self.assertEqual(IMAGE_TITLE, topic_page.topic.get_image_atr("title"))
        self.assertEqual(u"", topic_page.topic.get_image_atr("align"))

    def test_create_topic_img_url_with_align_left(self):
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_image()
        self.create_form.toolbar.image_form.select_link()
        self.create_form.toolbar.image_form.set_image_path_url(URL_IMAGE)
        self.create_form.toolbar.image_form.set_align(LEFT)
        self.create_form.toolbar.image_form.submit_image_upload_link()
        self.create_form.submit()

        topic_page = TopicPage(self.driver)
        self.assertIsNotNone(topic_page.topic.get_image_atr("src"))
        self.assertEqual(u"left", topic_page.topic.get_image_atr("align"))

    def test_create_topic_img_url_with_align_right(self):
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_image()
        self.create_form.toolbar.image_form.select_link()
        self.create_form.toolbar.image_form.set_image_path_url(URL_IMAGE)
        self.create_form.toolbar.image_form.set_align(RIGHT)
        self.create_form.toolbar.image_form.submit_image_upload_link()
        self.create_form.submit()

        topic_page = TopicPage(self.driver)
        self.assertIsNotNone(topic_page.topic.get_image_atr("src"))
        self.assertEqual(u"right", topic_page.topic.get_image_atr("align"))

    def test_create_topic_img_url_with_align_center(self):
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_image()
        self.create_form.toolbar.image_form.select_link()
        self.create_form.toolbar.image_form.set_image_path_url(URL_IMAGE)
        self.create_form.toolbar.image_form.set_align(CENTER)
        self.create_form.toolbar.image_form.submit_image_upload_link()
        self.create_form.submit()

        topic_page = TopicPage(self.driver)
        self.assertIsNotNone(topic_page.topic.get_image_atr("src"))
        if self.name == 'CHROME':
            self.assertEqual(u"center", topic_page.topic.get_image_atr("align"))
        if self.name == 'FIREFOX':
            self.assertEqual(u"middle", topic_page.topic.get_image_atr("align"))

    def test_create_topic_with_link(self):
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_link_in_text(LINK)
        self.create_form.toolbar.set_text_clicked(NAME_OF_LINK)
        self.create_form.submit()
        topic_page = TopicPage(self.driver)
        self.assertEqual(LINK, topic_page.topic.get_href_from_text(NAME_OF_LINK))

    def test_create_topic_with_user(self):
        self.create_form.set_prepare_fields(BLOG, TITLE)
        self.create_form.toolbar.select_user()
        self.create_form.toolbar.set_search_user(LINK_USER_NAME)
        self.create_form.submit()
        topic_page = TopicPage(self.driver)
        self.assertEqual(LINK_USER_PROFILE, topic_page.topic.get_href_from_text(LINK_USER_NAME))
