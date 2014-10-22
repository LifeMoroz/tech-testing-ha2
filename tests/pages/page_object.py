# coding=utf-8
import time

__author__ = 'ruslan'
import urlparse
from selenium.webdriver.common.action_chains import ActionChains
from components import *
from selenium.webdriver.support import expected_conditions


class TopMenu(Component):
    EMAIL = (By.CSS_SELECTOR, '#PH_user-email')

    def get_email(self):
        return WebDriverWait(self.driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda d: d.find_element(*self.EMAIL).text
        )


class Page(Component):
    BASE_URL = 'https://target.mail.ru'
    PATH = ''

    @property
    def top_menu(self):
        return TopMenu(self.driver)

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class AuthPage(Page):
    PATH = '/login'

    @property
    def _form(self):
        return AuthForm(self.driver)

    def fill_form(self, login, domain, pwd):
        form = self._form
        form.set_login(login)
        form.set_domain(domain)
        form.set_password(pwd)

        form.submit()

    def login(self, login, domain, pwd):
        """

        :param login:
        :param domain:
        :param pwd:
        :return:
        """
        self.fill_form(login, domain, pwd)

        create_page = CreateAdPage(self.driver)
        create_page.open()

        email = create_page.top_menu.get_email()
        return email == login + domain


class Campaign(Component):
    CAMPAIGN_ID = (By.CLASS_NAME, 'campaign-title__id')
    CAMPAIGN_DELETE = (By.CSS_SELECTOR, 'span.control__preset_delete')

    @staticmethod
    def get_campaign(driver, ):
        return Campaign()

    def __init__(self, driver, campaign, campaign_name):
        Component.__init__(self, driver)
        self.campaign = campaign

        self.campaign_name = campaign_name
        self._campaign_id = None

    @property
    def campaign_id(self):
        if self._campaign_id is None:
            self._campaign_id = self.campaign.find_element(*self.CAMPAIGN_ID).text[:-1]  # removing extra comma
        return self._campaign_id

    def edit(self):
        """
        :return: Campaign Edit page
        :rtype: tests.pages.edit_ad.EditAdPage
        """
        edit_page = EditAdPage(self.driver, self.campaign_id)
        edit_page.open()
        edit_page.wait_for_load()
        return edit_page

    def delete(self):
        delete_button = self.campaign.find_element(*self.CAMPAIGN_DELETE)
        delete_button.click()


class CreateAdPage(Page):
    PATH = '/ads/create'

    PAGE_CONTENT = (By.CLASS_NAME, 'create-page')
    SUBMIT_CAMPAIGN_BUTTON = (By.CLASS_NAME, 'main-button__label')

    def open(self):
        Page.open(self)
        self.wait_for_load()

    @property
    def campaign_base_settings(self):
        return CampaignBaseSettings(self.driver)

    @property
    def banner_form(self):
        return BannerForm(self.driver)

    @property
    def banner_preview(self):
        return BannerPreview(self.driver)

    @property
    def sex_targeting(self):
        return SexTargeting(self.driver)

    @property
    def where_targeting(self):
        return WhereTargeting(self.driver)

    def submit_campaign(self):
        self.driver.find_element(*self.SUBMIT_CAMPAIGN_BUTTON).click()

    def wait_for_load(self):
        self.wait_for_item_load(*self.PAGE_CONTENT)


class CampaignBaseSettings(Component):
    CAMPAIGN_NAME_INPUT = (By.CLASS_NAME, 'base-setting__campaign-name__input')

    @property
    def product_type(self):
        return ProductType(self.driver)

    @property
    def pad_type(self):
        return PadType(self.driver)

    def set_campaign_name(self, campaign_name):
        campaign_input = self.driver.find_element(*self.CAMPAIGN_NAME_INPUT)
        campaign_input.clear()
        campaign_input.send_keys(campaign_name)

    def set_product_type(self, product_name):
        self.product_type.select(product_name)

    def set_pad_type(self, pad_name):
        self.pad_type.select(pad_name)


class BannerForm(BannerComponent):
    SAVE_BANNER_BUTTON = (By.CLASS_NAME, 'banner-form__save-button')

    def __init__(self, driver):
        BannerComponent.__init__(self, driver)

    def wait_for_banner_close(self):
        WebDriverWait(self.driver, 1, 0.1).until(expected_conditions.element_to_be_clickable(self.SAVE_BANNER_BUTTON))

    def set_url(self, url):
        url_input = self._find_visible_element(None, self.URL_INPUT)
        url_input.send_keys(url)

    def set_image(self, image_uri):
        img_input = self.driver.find_element(*self.IMAGE_INPUT)
        img_input.send_keys(os.path.abspath(image_uri))

        BannerPreview.wait_for_cropper(self.driver)
        self.driver.find_element(*self.IMAGE_SUBMIT).click()
        self.wait_for_banner_close()

    def set_title(self, title):
        title_input = self.driver.find_element(*self.TITLE_INPUT)
        title_input.send_keys(title)

    def set_text(self, text):
        text_input = self.driver.find_element(*self.TEXT_TEXTAREA)
        text_input.send_keys(text)

    def submit(self):
        time.sleep(0.2)
        self.driver.find_element(*self.SAVE_BANNER_BUTTON).click()
        return BannerPreview(self.driver)

    def fill_banner(self, title, text, url, image_uri):
        """
        :return: Banner preview that is in added_banners section on page
        :rtype: BannerPreview
        """
        self.set_title(title)
        self.set_text(text)
        self.set_url(url)
        self.set_image(image_uri)
        return self.submit()


class BannerPreview(BannerComponent):
    ADDED_BANNERS = (By.CSS_SELECTOR, '.added-banner__banners-wrapper>li')
    BANNER_FORM = (By.CSS_SELECTOR, '.banner-form.free-block')
    BANNER_CROPPER = (By.CLASS_NAME, "image-cropper")
    PREVIEW_IMAGE = (By.CSS_SELECTOR, ".create-page__added-banners .banner-preview__wrapper[data-name='image']")
    PREVIEW_EDIT_BUTTON = (By.CSS_SELECTOR, '.added-banner__buttons-panel .added-banner__button_edit')
    URL_INPUT = (By.CSS_SELECTOR, '.banner-form__row[data-name=url][style="display: list-item;"] input[type=text]')
    BANNER_CLOSE = (By.CSS_SELECTOR, ".banner-form__close")

    def __init__(self, driver):
        BannerComponent.__init__(self, driver)
        banners = WebDriverWait(self.driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda d: d.find_elements(*self.ADDED_BANNERS)
        )
        if len(banners) == 1:
            self.banner = banners[0]
        else:
            raise Exception('Count of banners is %d instead of 1 somehow' % len(banners))

    def get_url(self):
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element(*self.PREVIEW_IMAGE))
        actions.click(on_element=self.driver.find_element(*self.PREVIEW_EDIT_BUTTON))
        actions.perform()

        banner_form = WebDriverWait(self.driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda b: b.find_element(*self.BANNER_FORM)
        )

        url_input = banner_form.find_element(*self.URL_INPUT).get_attribute('value')
        self.driver.find_element(*self.BANNER_CLOSE).click()
        return url_input

    @staticmethod
    def wait_for_cropper(driver):
        WebDriverWait(driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda b: b.find_element(*BannerPreview.BANNER_CROPPER)
        )


class SexTargeting(TargetingComponent):
    TARGETING_NAME = u'Пол'

    CHECKBOXES = (By.NAME, 'input')
    SEX_TARGETINGS = {
        u'Женщины': 'sex-F',
        u'Мужчины': 'sex-M'
    }

    def _get_value_and_wrapper(self):
        header = self.wait_for_item_load(*(By.XPATH, self.SETTING_HEADER_TEMPLATE % self.TARGETING_NAME))
        value_wrapper = header.find_element(By.XPATH, './../..').find_element(By.CLASS_NAME, 'campaign-setting__wrapper')

        value = WebDriverWait(value_wrapper, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(
            lambda d: d.find_element(By.CLASS_NAME, 'campaign-setting__value')
        )

        return value, value_wrapper

    def toggle_wrapper(self):
        value, value_wrapper = self._get_value_and_wrapper()
        WebDriverWait(self.driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until(lambda x: value.is_enabled())
        value.click() # toggle the targeting list
        return self

    def _get_content(self):
        _, value_wrapper = self._get_value_and_wrapper()
        content = value_wrapper.find_element(By.CSS_SELECTOR, '.campaign-setting__content .campaign-setting__detail')
        return content

    def toggle(self, sex):
        content = self._get_content()

        checkbox_input = content.find_element(By.ID, SexTargeting.SEX_TARGETINGS[sex])
        checkbox_input.click()

    def check_chosen(self, sex):
        content = self._get_content()

        not_chosen = []
        for s in sex:
            checkbox_input = content.find_element(By.ID, SexTargeting.SEX_TARGETINGS[s])
            if not checkbox_input.is_selected():
                not_chosen.append(s)

        return len(not_chosen) == 0, not_chosen

    def get_header_text(self):
        _, value_wrapper = self._get_value_and_wrapper()
        return value_wrapper.find_element(By.CLASS_NAME, 'campaign-setting__value').text


class WhereTargeting(TargetingComponent):
    REGION_CHECKBOX = '#regions%s > .tree__node__input'
    CHOSEN_BOX = '.campaign-setting__chosen-box__item[data-id="%s"]'

    def toggle(self, region_id):
        self.driver.find_element(By.CSS_SELECTOR, self.REGION_CHECKBOX % region_id).click()

    def check_chosen_by_id(self, region_id):
        return self.driver.find_element(By.CSS_SELECTOR, self.REGION_CHECKBOX % region_id).is_selected()

    def check_in_chosen_box(self, where):
        not_chosen = []
        for k, v in REGIONS_ID.items():
            chosen = self.driver.find_elements(By.CSS_SELECTOR, self.CHOSEN_BOX % v)
            if not chosen and k in where:
                not_chosen.append(k)

        return len(not_chosen) == 0, not_chosen

    def clear_all(self):
        WebDriverWait(self.driver, WEB_DRIVER_DEFAULT_WAIT, WEB_DRIVER_POLL_FREQ).until_not(
            lambda x: x.find_element(By.CSS_SELECTOR, ".tree .spinner"))
        for val in REGIONS_ID.values():
            if self.check_chosen_by_id(val):
                self.toggle(val)


class EditAdPage(CreateAdPage):
    PATH = 'ads/campaigns/%s/edit/'

    def __init__(self, driver, campaign_id):
        CreateAdPage.__init__(self, driver)
        self.PATH = self.PATH % campaign_id

    @property
    def base_settings(self):
        return EditAdBaseSettings(self.driver)


class CampaignsPage(Page):
    PATH = '/ads/campaigns'

    @property
    def campaigns_list(self):
        return CampaignsList(self.driver)


class CampaignsList(Component):
    CAMPAIGN_XPATH_TEMPLATE = ".//span[@class='campaign-title__name'][text()='%s']/ancestor::li[@class='campaign-row']"

    def get_campaign(self, campaign_name):
        campaign = self.wait_for_item_load(By.XPATH, self.CAMPAIGN_XPATH_TEMPLATE % campaign_name)
        return Campaign(self.driver, campaign, campaign_name)
