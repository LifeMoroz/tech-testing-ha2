# coding=utf-8
__author__ = 'ruslan'
from tests.config import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class Component:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_item_load(self, by, selector):
        return self.wait_for_item_load_by_parent(self.driver, by, selector)

    @staticmethod
    def wait_for_item_load_by_parent(parent, by, selector):
        return WebDriverWait(parent, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda d: d.find_element(by, selector)
        )

    def _find_visible_element(self, parent, selector):
        if parent is None:
            parent = self.driver

        elems = WebDriverWait(parent, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda p: p.find_elements(*selector)
        )
        elem = None
        for e in elems:
            if e.is_displayed():
                elem = e
                break
        if elem is None:
            raise Exception("Couldn't find visible to user element")
        return elem


class AuthForm(Component):
    LOGIN = (By.ID, 'id_Login')
    PASSWORD = (By.ID, 'id_Password')
    DOMAIN = (By.ID, 'id_Domain')
    SUBMIT = (By.CSS_SELECTOR, '#gogogo > .submit')

    def set_login(self, login):
        self.driver.find_element(*self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element(*self.PASSWORD).send_keys(pwd)

    def set_domain(self, domain):
        select = self.driver.find_element(*self.DOMAIN)
        Select(select).select_by_visible_text(domain)

    def submit(self):
        self.driver.find_element(*self.SUBMIT).click()


class RadioInput(Component):
    LABELED_INPUT_XPATH = ".//label[text() = '%s']/../input"

    def __init__(self, driver, type):
        Component.__init__(self, driver)
        self.type = type

    def select(self, product_name):
        products = self.driver.find_element(*self.type)
        radio_input = products.find_element(By.XPATH, self.LABELED_INPUT_XPATH % product_name)
        radio_input.click()


class ProductType(RadioInput):
    PRODUCT_TYPES = (By.CSS_SELECTOR, ".base-setting__product-type")

    def __init__(self, driver):
        RadioInput.__init__(self, driver, ProductType.PRODUCT_TYPES)


class PadType(RadioInput):
    TARGETING_TYPES = (By.CSS_SELECTOR, ".base-setting__pads-targeting")

    def __init__(self, driver):
        RadioInput.__init__(self, driver, PadType.TARGETING_TYPES)


class BannerComponent(Component):
    URL_INPUT = (By.XPATH, ".//input[@type='text'][@data-name='url']")
    IMAGE_INPUT = (By.XPATH, ".//input[@type='file'][@data-name='image']")
    TITLE_INPUT = (By.XPATH, ".//input[@type='text'][@data-name='title']")
    TEXT_TEXTAREA = (By.XPATH, ".//textarea[@data-name='text']")
    IMAGE_SUBMIT = (By.XPATH, u".//input[@type='submit'][@value='Сохранить изображение']")


class TargetingComponent(Component):
    SETTING_HEADER_TEMPLATE = "//span[@class='campaign-setting__name'][text() = '%s']"

    def __init__(self, driver):
        Component.__init__(self, driver)


class EditAdBaseSettings(Component):
    CAMPAIGN_NAME_INPUT = (By.CLASS_NAME, 'base-setting__campaign-name__input')
    PAD_VALUE = (By.CSS_SELECTOR, 'label.base-setting__pads-item__label')

    def get_campaign_name(self):
        campaign_input = self.driver.find_element(*self.CAMPAIGN_NAME_INPUT)
        return campaign_input.get_attribute('value')

    def get_pad(self):
        pad_label = self.driver.find_element(*self.PAD_VALUE)
        return pad_label.text