# -*- coding: utf-8 -*-

import urlparse
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class Page(object):
    BASE_URL = 'http://ftest.stud.tech-mail.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()


class AuthPage(Page):
    PATH = ''

    @property
    def form(self):
        return AuthForm(self.driver)

    @property
    def top_menu(self):
        return TopMenu(self.driver)


class CreatePage(Page):
    PATH = '/blog/topic/create/'

    @property
    def form(self):
        return CreateForm(self.driver)


class TopicPage(Page):
    @property
    def topic(self):
        return Topic(self.driver)

    @property
    def comment(self):
        return Comment(self.driver)


class BlogPage(Page):
    @property
    def topic(self):
        return Topic(self.driver)


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(Component):
    LOGIN = '//input[@name="login"]'
    PASSWORD = '//input[@name="password"]'
    SUBMIT = '//span[text()="Войти"]'
    LOGIN_BUTTON = '//a[text()="Вход для участников"]'

    def open_form(self):
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class TopMenu(Component):
    USERNAME = '//a[@class="username"]'

    def get_username(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.USERNAME).text
        )


class ImageForm(Component):
    PC = '//li[@data-type="pc"][1]/a'
    IMG_INPUT_FILE = '//input[@id="img_file"]'
    SUBMIT_IMAGE_UPLOAD = '//button[@id="submit-image-upload"]'
    SUBMIT_IMAGE_UPLOAD_LINK = '//button[@id="submit-image-upload-link"]'
    SUBMIT_IMAGE_UPLOAD_LINK_UPLOAD = '//button[@id="submit-image-upload-link-upload"]'
    LINK = '//li[@data-type="link"][1]/a'
    IMG_INPUT_URL = '//input[@id="img_url"]'
    IMG_TITLE = '//input[@id="form-image-url-title"][@name="title"]'
    IMAGE_ALIGN = '//select[@id="form-image-url-align"]'
    IMAGE_ALIGN_OPTION = '//option[text()="{}"]'

    def select_pc(self):
        self.driver.find_element_by_xpath(self.PC).click()

    def set_image_path_pc(self, src):
        path = os.path.abspath(src)        
        if os.path.exists(path):
            self.driver.find_element_by_xpath(self.IMG_INPUT_FILE).send_keys(path)

    def submit_image_upload(self):
        self.driver.find_element_by_xpath(self.SUBMIT_IMAGE_UPLOAD).click()
        WebDriverWait(self.driver, 5, 0.1).until(
            EC.invisibility_of_element_located((By.XPATH, self.SUBMIT_IMAGE_UPLOAD))
        )

    def select_link(self):
        self.driver.find_element_by_xpath(self.LINK).click()

    def set_image_path_url(self, url):
        self.driver.find_element_by_xpath(self.IMG_INPUT_URL).send_keys(url)

    def submit_image_upload_link(self):
        self.driver.find_element_by_xpath(self.SUBMIT_IMAGE_UPLOAD_LINK).click()
        WebDriverWait(self.driver, 5, 0.1).until(
            EC.invisibility_of_element_located((By.XPATH, self.SUBMIT_IMAGE_UPLOAD_LINK))
        )

    def submit_image_upload_link_upload(self):
        self.driver.find_element_by_xpath(self.SUBMIT_IMAGE_UPLOAD_LINK_UPLOAD).click()
        WebDriverWait(self.driver, 5, 0.1).until(
            EC.invisibility_of_element_located((By.XPATH, self.SUBMIT_IMAGE_UPLOAD_LINK_UPLOAD))
        )

    def set_image_url_title(self, title):
        self.driver.find_element_by_xpath(self.IMG_TITLE).send_keys(title)

    def set_align(self, option_text):
        select = Select(self.driver.find_element_by_xpath(self.IMAGE_ALIGN))
        select.select_by_visible_text(option_text)


class ToolBar(Component):
    FIND_BY_TEXT = '//*[contains(text(), "%s")]'
    TEXT = '//textarea[@id="id_text"]'
    H4 = '(//a[@title="H4"])[2]'
    H5 = '(//a[@title="H5"])[2]'
    H6 = '(//a[@title="H6"])[2]'
    STRONG = '(//a[@title="жирный [Ctrl+B]"])[2]'
    EM = '(//a[@title="курсив [Ctrl+I]"])[2]'
    S = '(//a[@title="зачеркнутый [Ctrl+S]"])[2]'
    U = '(//a[@title="подчеркнутый [Ctrl+U]"])[2]'
    BLOCKQUOTE = '(//a[@title="цитировать [Ctrl+Q]"])[2]'
    CODE = '(//a[@title="код"])[2]'
    LIST_UL = '(//a[@title="Список"])[3]'
    LIST_OL = '(//a[@title="Список"])[4]'
    IMAGE = '(//a[@title="изображение [Ctrl+P]"])[2]'
    LINK_IN_TEXT = '(//a[@title="Ссылка [Ctrl+L]"])[2]'
    USER = '(//a[@title="Пользователь"])[2]'
    SEARCH_USER_LOGIN_POPUP = '(//input[@id="search-user-login-popup"])'

    def click(self, field):
        self.driver.find_element_by_xpath(field).click()

    def select_h4(self):
        self.click(self.H4)

    def select_h5(self):
        self.click(self.H5)

    def select_h6(self):
        self.click(self.H6)

    def select_strong(self):
        self.click(self.STRONG)

    def select_em(self):
        self.click(self.EM)

    def select_s(self):
        self.click(self.S)

    def select_u(self):
        self.click(self.U)

    def select_blockquote(self):
        self.click(self.BLOCKQUOTE)

    def select_code(self):
        self.click(self.CODE)

    def select_list_ul(self):
        self.click(self.LIST_UL)

    def select_list_ol(self):
        self.click(self.LIST_OL)

    def select_ctrl_key(self, key):
        self.click(self.TEXT)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(key).key_up(Keys.CONTROL).perform()

    def select_image(self):
        self.driver.find_element_by_xpath(self.IMAGE).click()

    def select_link_in_text(self, link):
        self.driver.find_element_by_xpath(self.LINK_IN_TEXT).click()
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')
            alert = self.driver.switch_to_alert()
            alert.send_keys(link)
            alert.accept()
        except TimeoutException:
            pass

    def select_user(self):
        self.driver.find_element_by_xpath(self.USER).click()

    def set_search_user(self, username):
        self.driver.find_element_by_xpath(self.SEARCH_USER_LOGIN_POPUP).send_keys(username)
        element = self.FIND_BY_TEXT % (username,)
        WebDriverWait(self.driver,10, 1).until(
            EC.element_to_be_clickable((By.XPATH, element))).click()

    def set_text_clicked(self, text):        
        ActionChains(self.driver).send_keys(text).perform()

    @property
    def image_form(self):
        return ImageForm(self.driver)


class Preview(Component):
    PREVIEW_ROLL_BUTTON = '//button[contains(text(),"свернуть")]'
    PREVIEW_BUTTON = '//button[contains(text(),"Предпросмотр")]'
    PUBLISH_BUTTON = '//button[contains(text(),"Опубликовать")]'
    PREVIEW_TEXT = '//div[@id="text_preview"]/article/div'

    def open(self):
        self.driver.find_element_by_xpath(self.PREVIEW_BUTTON).click()

    def close(self):
        self.driver.find_element_by_xpath(self.PREVIEW_ROLL_BUTTON).click()

    def select_publish_topic(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, self.PUBLISH_BUTTON)))
        element.click()

    def get_preview_text(self):
        return WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(self.PREVIEW_TEXT).text
        )


class CreateForm(Component):

    @property
    def toolbar(self):
        return ToolBar(self.driver)

    @property
    def preview(self):
        return Preview(self.driver)

    BLOGSELECT = '//a[@class="chzn-single"]'
    OPTION = '//li[text()="{}"]'
    TITLE = '//input[@name="title"]'
    TEXT = '//textarea[@id="id_text"]'
    CREATE_BUTTON = '//button[contains(text(),"Создать")]'
    MESSAGE_ERROR = '//ul[@class="system-message-error"][1]'
    ADD_POLL = '//input[@name="add_poll"]'  
    QUESTION = '//input[@id="id_question"][@name="question"]'    
    ANSWERS = '//input[@id="id_form-%s-answer"][@name="form-%s-answer"]'
    ADD_ANSWER = '//a[@class="add-poll-answer link-dotted"]'
    DRAFT = '//input[@id="id_publish"]'
    EDITING = '//a[class="actions-edit"]'
    FIND_BY_TEXT = '//*[contains(text(), "%s")]'
    DISALLOW_COMMENT = '//input[@id="id_forbid_comment"]'

    def with_wait(self, arg):
        return WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(arg).text
        )

    def select_draft(self):
        self.driver.find_element_by_xpath(self.DRAFT).click()

    def select_disallow_comment(self):
        self.driver.find_element_by_xpath(self.DISALLOW_COMMENT).click()

    def select_add_poll(self):
        self.driver.find_element_by_xpath(self.ADD_POLL).click()       

    def steps_left(self, steps):  
        for x in range(0, steps):                    
            ActionChains(self.driver).key_down(Keys.LEFT).perform()

    def blog_select_open(self):
        self.driver.find_element_by_xpath(self.BLOGSELECT).click()

    def blog_select_set_option(self, option_text):
        self.driver.find_element_by_xpath(self.OPTION.format(option_text)).click()

    def set_title(self, title):
        self.driver.find_element_by_xpath(self.TITLE).send_keys(title)

    def set_text_not_clicked(self, text):
        self.driver.find_element_by_xpath(self.TEXT).click()
        ActionChains(self.driver).send_keys(text).perform()

    def set_text_clicked(self, text):
        self.driver.find_element_by_xpath(self.TEXT)
        ActionChains(self.driver).send_keys(text).perform()

    def set_question(self, text):
        wait = WebDriverWait(self.driver, 10)
        question = wait.until(EC.visibility_of_element_located((By.XPATH,self.QUESTION)))
        question.send_keys(text)

    def set_answers(self, num, text):
        answers = self.ANSWERS % (num,num,)        
        self.driver.find_element_by_xpath(answers).click()
        ActionChains(self.driver).send_keys(text).perform()

    def submit(self):        
        WebDriverWait(self.driver,10, 1).until(
            EC.visibility_of_element_located((By.XPATH, self.CREATE_BUTTON))).click()

    def is_message_error(self):
        try:
            return self.driver.find_element_by_xpath(self.MESSAGE_ERROR).is_displayed()
        except NoSuchElementException:
            return False

    def set_prepare_fields(self, option_text, title):
        if option_text != "":
            self.blog_select_open()
            self.blog_select_set_option(option_text)
        self.set_title(title)

    def set_all_fields(self, option_text, title, text):
        self.set_prepare_fields(option_text, title)
        self.set_text_not_clicked(text)

    def get_text(self):
        text = self.driver.find_elements_by_xpath(self.TEXT)
        return text[0].get_attribute("value")


class EditForm(Component):
    TEXT = '//textarea[@id="id_text"]'
    TITLE = '//input[@name="title"]'
    STORE_BUTTON = '//button[contains(text(),"Сохранить")]'

    def set_title(self, title):
        self.driver.find_element_by_xpath(self.TITLE).send_keys(title)

    def set_text_not_clicked(self, text):
        self.driver.find_element_by_xpath(self.TEXT).click()
        ActionChains(self.driver).send_keys(text).perform()

    def store(self):
        self.driver.find_element_by_xpath(self.STORE_BUTTON).click()


class Comment(Component):
    COMMENT_POST = '//a[contains(text(),"Оставить комментарий")]'
    TEXT = '//textarea[@id="id_text"]'
    SUBMIT_COMMENT = '//button[contains(text(),"добавить")]'

    def select_post_comment(self):
        try:
            self.driver.find_element_by_xpath(self.COMMENT_POST).click()
            return True
        except NoSuchElementException:
            return False

    def set_comment(self, text):
        self.driver.find_element_by_xpath(self.TEXT).click()
        ActionChains(self.driver).send_keys(text).perform()

    def submit_comment(self):
        self.driver.find_element_by_xpath(self.SUBMIT_COMMENT).click()


class Topic(Component):

    TITLE = '//*[@class="topic-title"]/a'
    TEXT = '//*[@class="topic-content text"]%s'
    BLOG = '//*[@class="topic-blog"]'
    AUTHOR = '//*[@class="topic-info-author"]/a[2]'
    FAVOURITE = '//span[@class="favourite-count"]'
    COMMENTS = '//li[@class="topic-info-comments"]/a[1]'
    NOTICE = '//div[@id="content"]/ul/li'
    DELETE_BUTTON = '//a[@class="actions-delete"]'
    DELETE_BUTTON_CONFIRM = '//input[@name="submit"][@type="submit"][@class="button button-primary"]'
    COMMENT = '(//div[@class="comment-rendered"])'
    DRAFT_ICON = '//i[@title="топик находится в черновиках"]'
    IMAGE = '//div[@class="topic-content text"]/img'
    FIND_BY_TEXT = '//*[contains(text(), "%s")]'

    def with_wait(self, arg):
        return WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(arg).text
        )

    def get_title(self):
        return self.with_wait(self.TITLE)

    def get_blog(self):
        return self.with_wait(self.BLOG)

    def get_text(self, tag=""):
        text = self.TEXT % (tag,)        
        return self.with_wait(text)      

    def get_username(self):
        return self.with_wait(self.AUTHOR)

    def get_favourite(self):
        return self.with_wait(self.FAVOURITE)       

    def get_comments_count(self):
        return self.with_wait(self.COMMENTS)

    def get_comments(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, self.COMMENT)))
        return element.text

    def get_notice(self): 
        return self.with_wait(self.NOTICE)

    def open_blog(self):
        self.driver.find_element_by_xpath(self.BLOG).click()

    def select_edit_topic(self):
        element = self.FIND_BY_TEXT % ("Редактировать",)
        self.driver.find_element_by_xpath(element).click()

    def is_draft_icon_displayed(self):
        try:
            return self.driver.find_element_by_xpath(self.DRAFT_ICON).is_displayed()
        except NoSuchElementException:
            return False

    def get_image_atr(self, atr):
        return self.driver.find_element_by_xpath(self.IMAGE).get_attribute(atr)

    def get_href_from_text(self, name_of_link):
        element = self.FIND_BY_TEXT % (name_of_link,)
        text = self.driver.find_elements_by_xpath(element)
        return text[0].get_attribute("href")

    def delete(self):
        WebDriverWait(self.driver,10, 1).until(
            EC.visibility_of_element_located((By.XPATH, self.DELETE_BUTTON))).click()
        WebDriverWait(self.driver,10, 1).until(
            EC.visibility_of_element_located((By.XPATH, self.DELETE_BUTTON_CONFIRM))).click()