# coding=utf-8
import unittest
from selenium.webdriver.common.by import By
from tests.basic_testcase import BasePage
from tests.config import *
from tests.pages.page_object import CreateAdPage, CampaignsPage


class AdEditTestCase(BasePage):
    @classmethod
    def setUpClass(cls):
        super(AdEditTestCase, cls).setUpClass()
        ad_page = CreateAdPage(cls.driver)
        cls._fill_basic_settings(ad_page)

        sex_sex_sex = ad_page.sex_targeting
        sex_sex_sex.toggle_wrapper()  # opening
        for hot_hot_hot in sex_sex_sex.SEX_TARGETINGS.keys():
            chosen = sex_sex_sex.check_chosen([hot_hot_hot])
            if (chosen and not hot_hot_hot in TEST_SEX_DATA) or (not chosen and hot_hot_hot in TEST_SEX_DATA):  # It can be already allocated
                sex_sex_sex.toggle(hot_hot_hot)

        where_targeting = ad_page.where_targeting
        where_targeting.clear_all()
        for where in TEST_WHERE_DATA:
            where_targeting.toggle(REGIONS_ID[where])

        ad_page.banner_form.fill_banner(**BANNER_DATA)
        ad_page.submit_campaign()

        cls.campaign = CampaignsPage(cls.driver)
        cls.editor = cls.campaign.campaigns_list.get_campaign(CAMPAIGN_NAME).edit()

    @classmethod
    def tearDownClass(cls):
        cls.campaign.open()
        cls.campaign.campaigns_list.get_campaign(CAMPAIGN_NAME).delete()

    def test_campaign_name_correct(self):
        """
            Проверка правильности имени кампании
        """
        name = self.editor.base_settings.get_campaign_name()
        self.assertEqual(CAMPAIGN_NAME, name)

    def test_pad_correct(self):
        """
            Проверка правильности площадки
        """
        pad = self.editor.base_settings.get_pad()
        self.assertEqual(PAD_TYPE, pad)

    def test_banner_preview_correct(self):
        """
            Проверка правильности данных в баннере
        """
        banner_preview = self.editor.banner_preview
        url = banner_preview.get_url()

        self.assertIn(BANNER_DATA['url'], url, "URL isn't correct")

    def test_where_in_chosen_box(self):
        """
            Проверка, что where в списке выделенных
        """
        where_targeting = self.editor.where_targeting
        where_targeting.clear_all()
        for where in TEST_WHERE_DATA:
            where_targeting.toggle(REGIONS_ID[where])

        chosen, not_chosen = where_targeting.check_in_chosen_box(TEST_WHERE_DATA)

        self.assertTrue(chosen, 'Some of the incomes have not been chosen: %s' % not_chosen)

    def test_sex_chosen(self):
        """
            Проверяет что выбран именно нужный пол
        """
        sex_sex_sex = self.editor.sex_targeting
        all_incomes_checked, not_checked = sex_sex_sex.check_chosen(TEST_SEX_DATA)

        self.assertTrue(all_incomes_checked, 'Some of the incomes have not been checked: %s' % not_checked)