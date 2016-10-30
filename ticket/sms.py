#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
for: send message to mobile
by hxer, 2015.12.2
method:
    [+] google calendar api新建事件，发短信 -- no use
    [+] mobile email to sms notify
"""

from __future__ import unicode_literals
from mail import Mail

class SMS(object):
    """
    """
    def __init__(self):
        pass

    def sendsms(self, msg=None):
        from_mail = "xxx@163.com"
        passwd = "xxx"
        to_mail_list = ["xx@xxx",]
        subject = 'ticket'
        text = msg if msg else 'to buy ticket, surpising'
        mail = Mail(from_mail, passwd)
        mail.sendplain(to_mail_list, subject, text)
