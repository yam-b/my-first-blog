# -*- coding: utf-8 -*-
import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from django.shortcuts import render

URL = 'http://www.handasaim.co.il'
TEXT_TO_FIND = u'מערכת שעות'
UP_CUT = 0
LEFT_CUT = 1
DEFAULT_INFO = u''


def b(link):
    news = bs(requests.get(link).content, 'lxml').find('marquee')
    return [i for i in news.find_all('b') if TEXT_TO_FIND in i.text][0]


def to_table(url):
    sheet = pd.ExcelFile(url).parse(0)
    return [sheet.iloc[i, LEFT_CUT:] for i in range(UP_CUT, len(sheet.index))]


def to_heb_month(month):
    return {
        '01': u'ינואר',
        '02': u'פברואר',
        '03': u'מרץ',
        '04': u'אפריל',
        '05': u'מאי',
        '06': u'יוני',
        '07': u'יולי',
        '08': u'אוגוסט',
        '09': u'ספטמבר',
        '10': u'אוקטובר',
        '11': u'נובמבר',
        '12': u'דצמבר',
    }[month]


def index(request):
    dude_error = 0
    # local = os.path.join(BASE_DIR, 'handaschedule/schedule.xlsx')
    try:
        title = b(URL).text.strip()
        link = b(URL).find_next_sibling('a')['href'].strip()
        time = b(URL).find_previous_sibling('sup').text[1:-1]
        time = time[:2] + u' ב' + to_heb_month(time[3:5])
        table = to_table(link)  # ONLINE: to_table(link) OFFLINE: to_table(local)
    except:
        table = []
        title = 'מערכת שעות'
        link = '#'
        time = datetime.date.today().strftime('%d ') + u'ב' + to_heb_month(datetime.date.today().strftime('%m'))
        dude_error = 1
    try:
        info = b(URL).next_sibling.strip()
    except:
        info = DEFAULT_INFO
    return render(request, 'handaschedule/index.html',
                  {'url': URL, 'title': title, 'info': info, 'link': link, 'time': time, 'table': table,
                   'error': dude_error})
