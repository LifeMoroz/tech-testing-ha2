# coding=utf-8

__author__ = 'ruslan'

from datetime import datetime
import os

_DATE_FORMATTER = '%d.%m.%Y'

DOMAIN = '@mail.ru'
USERNAME = 'tech-testing-ha2-7'
PASSWORD = os.environ.get('TTHA2PASSWORD')

CAMPAIGN_NAME = 'My Test Campaign 2014'
PRODUCT_TYPE = u'Группа, событие, видеоканал'
PAD_TYPE = u'Одноклассники: веб-версия'
BANNER_DATA = {
    'title': 'My Title',
    'text': 'Description',
    'url': 'http://odnoklassniki.ru/group/123',
    'image_uri': os.path.dirname(__file__) + '/res/img2.jpg'
}

TEST_SEX_DATA = [u'Мужчины']

REGIONS_ID = {
    'Russia': '188',
    'USSR': '100001',
    'Europa': '100002',
    'Asia': '100003',
    'North America': '100005',
    'Others': '100009'
}

TEST_WHERE_DATA = ['USSR']

FROM_DATE = datetime.strptime('01.01.2015', _DATE_FORMATTER)
TO_DATE = datetime.strptime('01.08.2015', _DATE_FORMATTER)

WEB_DRIVER_DEFAULT_WAIT = 5
WEB_DRIVER_POLL_FREQ = 0.1