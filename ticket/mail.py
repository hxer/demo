#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
for: mail something
by hxer, 2015.12.2
"""

from __future__ import unicode_literals
#from __future__ import print_function
import smtplib
from email.mime.text import MIMEText
from email.header import Header    #解决中文编码
import logging

class Mail(smtplib.SMTP):
    """
    """
    def __init__(self, user, passwd):
        smtplib.SMTP.__init__(self)
        self.set_debuglevel(True)
        self.fromaddr = user
        try:
            self.connect("smtp.163.com",port=25)
            self.login(user, passwd)
        except Exception as e:
            logging.Error("163 connect error: %s", e)

    def sendplain(self, to_list, subject, text):
        """
        """
        msg=MIMEText(text, 'plain', 'utf-8')
        msg['From']=self.fromaddr
        #msg['To']接收的是字符串而不是list，多个地址用","隔开
        msg['To']=','.join(to_list)
        msg['Subject'] = Header(subject,'utf-8').encode()
        self.sendmail(self.fromaddr, to_list, msg.as_string())

if __name__ == "__main__":
    pass
    """Example:
        from_mail = "xxx@xxx.com"
        passwd = "xxxx"
        to_mail_list = ["xxx@xxx.com","xxx@qxx.com"]
        subject = 'from python'
        text = 'have a ticket'
        mail = Mail(from_mail, passwd)
        mail.sendplain(to_mail_list, subject, text)
    """



