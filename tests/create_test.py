# coding=utf-8
import unittest
from tests.basic_testcase import BasePage

from pages.page_object import *
from tests.config import *


class AdCreationTestCase(BasePage):
    ad_page = None

    @classmethod
    def setUpClass(cls):
        super(AdCreationTestCase, cls).setUpClass()
        ad_page = CreateAdPage(cls.driver)
        cls._fill_basic_settings(ad_page)
        ad_page.banner_form.fill_banner(**BANNER_DATA)
        AdCreationTestCase.ad_page = ad_page

    def test_banner_preview(self):
        """
            Проверяет правильность данных в отправленном баннере
        """
        banner_preview = AdCreationTestCase.ad_page.banner_preview
        url = banner_preview.get_url()

        self.assertEqual(BANNER_DATA['url'], url, "Entered url doesn't match the one in banner_preview")

    def test_sex_on_toggling(self):
        """
            Проверка того, что данные в sex сохраняются при сворачивании списка настроек
        """
        sex_sex_sex = AdCreationTestCase.ad_page.sex_targeting
        sex_sex_sex.toggle_wrapper()  # opening
        for hot_hot_hot in sex_sex_sex.SEX_TARGETINGS.keys():
            chosen = sex_sex_sex.check_chosen([hot_hot_hot])
            if (chosen and not hot_hot_hot in TEST_SEX_DATA) or (not chosen and hot_hot_hot in TEST_SEX_DATA):  # It can be already allocated
                sex_sex_sex.toggle(hot_hot_hot)

        sex_sex_sex.toggle_wrapper()  # closing
        all_incomes_checked, not_checked = sex_sex_sex.check_chosen(TEST_SEX_DATA)

        self.assertTrue(all_incomes_checked, 'Some of the incomes have not been checked: %s' % not_checked)

    def test_where_in_chosen_box(self):
        """
            Проверка, что после выделения where попала в список выделенных
        """
        where_targeting = AdCreationTestCase.ad_page.where_targeting
        where_targeting.clear_all()
        for where in TEST_WHERE_DATA:
            where_targeting.toggle(REGIONS_ID[where])

        chosen, not_chosen = where_targeting.check_in_chosen_box(TEST_WHERE_DATA)

        self.assertTrue(chosen, 'Some of the incomes have not been chosen: %s' % not_chosen)