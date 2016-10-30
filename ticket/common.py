#-*- coding:utf-8 -*-

"""
by hxer, 2015.12.2
"""

from __future__ import unicode_literals
import requests
import logging
import os.path
import ConfigParser
import sys
import datetime

# Set default encoding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')
requests.packages.urllib3.disable_warnings()

SEATCODE = {
    '特等' : 'P',
    '商务座': '9',
    '一等座': 'M',
    '二等座': 'O',
    '硬座': '1',
    '硬卧': '3',
    '软卧': '4'
}
SEATTYPE = {
    '商务座':'swz',
    '特等座':'tz',
    '一等座':'zy',
    '二等座':'ze',
    '高级软卧':'gr',
    '软卧':'rw',
    '硬卧':'yw',
    '软座':'rz',
    '硬座':'yz',
    '无座':'wz',
}

class Base12306(object):
    """
    """
    def __init__(self):
        """
        """
        host = 'kyfw.12306.cn'
        baseurl = "https://" + host + "/otn/"
        self.headers = {
            'Host': host,
            'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:42.0) Gecko/20100101 Firefox/42.0 FirePHP/0.7.4',
            'X-Requested-With':'XMLHttpRequest',
            'Referer': baseurl,
        }
        """
        12306页面存在两种查询：车票预订查询和余票查询
        两种查询的链接不一样，查询结果是否有差异，暂不知
        """
        self.urls = {
            'query': baseurl + 'lcxxcx/query',          #余票查询
            'bookquery': baseurl + 'leftTicket/queryT', #预订查询
            'stations': baseurl + "resources/js/framework/station_name.js"
        }

        self.session = requests.Session()

    def geturl(self, url, params=None):
        """
        """
        try:
            response = self.session.get(url, headers=self.headers, params=params, timeout=8, verify=False)
            return response
        except requests.exceptions.HTTPError as e:
            logging.error("HTTP Error: %s", e)
            return None

    def getstations(self):
        """
        每个站的格式如下:
        @bji|北京|BJP|beijing|bj|2   ---> @拼音缩写三位|站点名称|编码|拼音|拼音缩写|序号
        """
        stations = {}
        if not os.path.isfile('station_name.js'):
            logging.info('start loading station_name.js')
            response = self.geturl(self.urls['stations'])
            assert response.status_code == 200
            with open('station_name.js', 'wb') as f:
                 f.write( response.content )
        else:
            logging.info('loading local station_name.js')
        with open('station_name.js', 'rb') as f:
            data = f.read().decode('utf-8')
            data = data.partition('=')[2].strip("'")    #var station_names ='..'
        for station in data.split('@')[1:]:
            items = station.split('|')      # bjb|北京北|VAP|beijingbei|bjb|0
            stations[ items[1] ] = items[2]
        return stations

    def readConfig(self, cfg):
        """
            params:
                cfg: class Config
        """
        conf = dict()
        conf['purpose_codes'] = cfg.purpose_codes
        conf['from_city_name'] = cfg.from_city_name
        conf['to_city_name'] = cfg.to_city_name
        conf['train_dates'] = self.parse_dates(cfg.train_dates)
        conf['station_train_code'] = cfg.station_train_code
        conf['seat_type'] = self.parse_seattype(cfg.seat_type)
        return conf

    def parse_seattype(self, seats):
        """
        """
        return [SEATTYPE[seat] for seat in seats if seat in SEATTYPE.keys()]

    def parse_dates(self, strdates):
        """
        """
        dates = []
        for date in strdates.split(','):
            if '...' in date:
                dates += self.transformdate(date.split('...'))
            else:
                dates.append(date)
        return dates

    def transformdate(self, daterange):
        """
        这里给了一个日期的开始和结束时间，最好的方式是自定义一个日期生成器，
        使用for循环产生日期列表
        """
        dates = []
        year, month, day = map(int, daterange[0].split('-'))
        date0 = datetime.date(year,month,day)
        year, month, day = map(int, daterange[1].split('-'))
        date1 = datetime.date(year,month,day)
        deltadate = datetime.timedelta(1)

        while date0 <= date1:
            dates.append(date0.isoformat())
            date0 += deltadate
        return dates


class Config(object):
    """
    """
    def __init__(self, config_file):
        """
        """
        cp = ConfigParser.ConfigParser()
        try:
            cp.readfp(open(config_file, 'r'))
        except IOError as e:
            logging.error('open config file %s: %s', config_file, e)

        self.purpose_codes = cp.get('train', 'purpose_codes')
        self.from_city_name = cp.get('train', 'from').decode('utf-8')
        self.to_city_name= cp.get('train', 'to').decode('utf-8')
        self.train_dates= cp.get('train', 'dates')
        self.station_train_code = cp.get('special', 'station_train_code').split(',')
        self.seat_type = cp.get('special', 'seattype').split(',')

        self.to_mail_list = cp.get('mail', 'emailaddr').split(',')
