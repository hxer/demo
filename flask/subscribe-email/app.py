#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import Flask
from flask import request
from flask import render_template
from flask import url_for


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/subscribe')
def subscribe():
    return render_template('email.html')


@app.route('/unsubscribe')
def unsubscribe():
    return render_template('email.html')

if __name__ == '__main__':
    app.run(debug=True)
