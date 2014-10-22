import unittest

from selenium.webdriver import DesiredCapabilities, Remote
from tests.pages.page_object import *
from tests.config import *


def login(driver):
    auth_page = AuthPage(driver)
    auth_page.open()
    logged_in = auth_page.login(USERNAME, DOMAIN, PASSWORD)
    if not logged_in:
        raise Exception("Couldn't login")


class BasePage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        cls.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        login(cls.driver)

    @staticmethod
    def _fill_basic_settings(ad_page):
        base_settings = ad_page.campaign_base_settings
        base_settings.set_campaign_name(CAMPAIGN_NAME)
        base_settings.set_product_type(PRODUCT_TYPE)
        base_settings.set_pad_type(PAD_TYPE)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()