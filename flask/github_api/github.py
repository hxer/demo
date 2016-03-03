# -*- coding: utf-8 -*-

import os

import requests
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import flash

app = Flask(__name__)
app.secret_key = os.urandom(24)

class Client(object):
    """
    """
    def __init__(self):
        self.id = "da43827a6b636a68e5ad"
        self.secret = "9b76611737f90572783350aa000d0c7a1cf901ca"


def get_userinfo(token):
    url = 'https://api.github.com/user?access_token={}'.format(token)
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get(url, headers=headers)
    return r


@app.route('/')
def index():

    # session state for safety about cross site attack
    if 'state' not in session:
        # generate random string
        session['state'] = ''.join(map(lambda x:(hex(ord(x))[2:]), os.urandom(16)))

    if 'access_token' in session:
        url = url_for('home')
    else:
        client = Client()
        redirect_url = "http://localhost:5000/callback"
        url = 'https://github.com/login/oauth/authorize?'
        url += 'client_id={id}&redirect_url={url}&state={state}'.format(
                    id=client.id, url=redirect_url, state=session['state'])

    return render_template('github_login.html', url=url)


@app.route('/callback', methods=['GET'])
def github_callback():
    """
    """
    client = Client()

    url = "https://github.com/login/oauth/access_token"
    redirect_url = "http://localhost:5000/callback"

    # code and state from github
    code = request.args.get('code')
    state = request.args.get('state')

    payload = {
        'client_id': client.id,
        'client_secret': client.secret,
        'code': code,
        'redirect_url': redirect_url
    }

    headers = {
        'Accept': 'application/json'
    }

    r = requests.post(url, data=payload, headers=headers)
    params = r.json()
    access_token = params.get('access_token')
    #scope = params.get('scope')

    # attck
    if state and state != session.get('state'):
        flash('Stop Hacking')
        return redirect(url_for('index'))
    elif access_token:
        session['access_token'] = access_token
        return redirect(url_for('home'))
    else:
        flash('github authorize error, please login again!')
        return redirect(url_for('index'))


@app.route('/user')
def home():
    info = {}

    if session.get('access_token'):
        r = get_userinfo(session['access_token'])
        params = r.json()
    else:
        params = {}

    info['name'] = params.get('name', 'None')
    info['id']  = params.get('id', 0)

    return render_template('user.html', url=url_for('logout'), info=info)


@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
