#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import subprocess
from subprocess import CalledProcessError
import sys

reload(sys)
sys.setdefaultencoding('utf8') 


def request(url):
    cmd = 'phantomjs request.js ' + url 
    #cmd.append(url)
    try:
        output = subprocess.check_output(cmd, shell=True)
    except CalledProcessError:
        # system return not zero
        print "[!Error] cmd error"
        return None

    if output.startswith('[!Failed]]'):
        print output
        return None
    else:
        return output


if __name__ == "__main__":
    url = "http://www.xicidaili.com"
    print request(url)
    