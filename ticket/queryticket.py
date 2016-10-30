#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
by hx, 2015.12.3
"""

from __future__ import unicode_literals
from __future__ import print_function
import logging
import sys
import time

from common import *
from sms import SMS
from mail import Mail

from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(filename="queryticket.log",
    level=logging.DEBUG,
    format='%(asctime)s|%(filename)s|%(funcName)s|line:%(lineno)d%(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M'
)


def printItem(items, name):
    msgs = items.get(name, "")
    if isinstance(msgs, list):
        for msg in msgs:
          print(msg)
    else:
        print(msgs)


class QueryTicket(Base12306):
    """
    """
    def __init__(self, cfg):
        """
            params:
                cfg: class Config
        """
        Base12306.__init__(self)
        self.stations = self.getstations()
        self.conf = self.readConfig(cfg)
        if not self.conf:
            logging.error("read conf error, system exiting")
            sys.exit()

    def querytickets(self, train_date):
        """
        """
        # parameters必须按如下指定顺序排列，否则返回结果为 -1
        parameters = [
            ('purpose_codes', self.conf['purpose_codes']),
            ('queryDate', train_date),
            ('from_station', self.stations[ self.conf['from_city_name']]),
            ('to_station', self.stations[ self.conf['to_city_name']]),
        ]
        response = self.geturl(self.urls['query'],params=parameters)
        if 200 != response.status_code and len(response.content) < 10:
            logging.error("request error code: %s, content: %s",
                response.status_code,response.content)
        try:
            jdata = response.json()
        except Exception as e:
            logging.error("parse json error: %s",e)
            return None
        else:
            return self.parsejson(jdata)


    def parsejson(self, jdata):
        """
        """
        traindict = dict()
        try:
            trains = jdata['data']['datas']
        except Exception as e:
            logging.error("get trains from json error: %s", e)
        for train in trains:
            if train['station_train_code'] in self.conf['station_train_code'] \
                or 'all' in self.conf['station_train_code']:
                #特殊查询待处理
                traindict[train['station_train_code']] = self.get_validseat(train)
        return traindict

    def get_validseat(self, train):
        """
        """
        return {seat:self.getnum(train[seat+'_num']) for seat in self.conf['seat_type'] if self.getnum(train[seat+'_num']) != '0'}

    def getnum(self, seatnum):
        """
        """
        return '0' if '无' in seatnum or '--' in seatnum else seatnum


def sendmail(cfg_file, subject, msg):
    """
    """
    cfg = Config(cfg_file)
    to_mail_list = cfg.to_mail_list
    from_mail = "xxx@163.com"
    passwd = "xxx"
    mail = Mail(from_mail, passwd)
    mail.sendplain(to_mail_list, subject, msg)

def task(cfg_file):
    """
    """
    cfg = Config(cfg_file)
    seatname = {value:key for key, value in SEATTYPE.items()}
    msg = ''
    #sms = SMS()
    qticket = QueryTicket(cfg)
    for train_date in qticket.conf['train_dates']:
        traindict = qticket.querytickets(train_date)
        if traindict:
            for train_code in traindict.keys():
                if traindict[train_code]:
                    msg = msg + train_date + '\t' + train_code
                    for seat, strnum in traindict[train_code].items():
                        msg = msg + '\n\t' + seatname[seat] + ':' + strnum + '张'
                    msg += '\n'
                    print(train_date, train_code,traindict[train_code])
                else:
                    print(train_date, train_code, " no ticket")
        time.sleep(10)
    if msg:
        print(msg)
        #sms.sendsms(train_date+train_code+str(traindict[train_code]))
        sendmail(cfg_file, '抢火车票了...from hxer', msg)

if __name__=="__main__":
    debug = False
    cfg_files = ["config1.ini","config2.ini"]
    if not debug:
        sched = BlockingScheduler()
        for cfg_file in cfg_files:
            sched.add_job(task, args=(cfg_file,), trigger="cron", hour='6-23', minute='0-59/10')
        try:
            sched.start()
        except:
            sched.shutdown()
    else:
        task(cfg_files[0])
        #sendmail('测试...from hxer', '测试')
        print("finished")

