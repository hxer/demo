# a demo for django with mongodb

A simple example of how-to build a blog with mongodb database, using django framework.

on ubuntu 16.04 x64 desktop.

## basic install

```python
pip install django==1.8.10
pip install pymongo
pip install mongoengine
```

使用前确保`mongodb`服务已经开启，然后运行`pyton manage.py runserver`,访问 [http://127.0.0.1:8000](http://127.0.0.1:8000).

## uwsgi + nginx + supervisor 部署

### virtualenv

```
pip install virtualenv
pip install virtualenvwrapper
```

edit `~/.bashrc`, then `source ~/.bashrc`.   
```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

```
mkvirtualenv mongodemo
pip install django==1.8.10
pip install pymongo
pip install mongoengine
pip install uwsgi

sudo cp -R ~/.virtualenvs/mongodemo/* /data/site/env/
```
### uwsgi

install: `sudo apt-get install python-dev, pip install uwsgi`

写`ini`配置文件`uwsgi8899.ini`.

`ini`示例文件：   
```
[uwsgi]
project = secondsite
base = /home/user

chdir = %(base)/%(project)
home = %(base)/Env/%(project)
module = %(project).wsgi:application

master = true
processes = 5

socket = %(base)/%(project)/%(project).sock
chmod-socket = 664
vacuum = true
```

### nginx

install:   
```
nginx=stable
add-apt-repository ppa:nginx/$nginx
apt-get update
apt-get install nginx
```

本目录下`ngnix.conf`替换掉`/etc/nginx/nginx.conf`文件，重启`ngnix服务`

### surpervisor

install: `pip install supervisor`

### run

```
python manage.py collectstatic
sudo service monogdb restart
sudo service ngnix restart
sudo supervisord -c /data/site/supervisord.conf
supervisorctl start uwsgi
```

visit: [http://127.0.0.1](http://127.0.0.1)

## note

* uwsgi uid pid

当执行`supervisord`命令的用户没有切换用户的权限时，要加上`sudo`，否则uwsgi开启的进程用户将是当前执行命令的用户，因为当前用户没有权限切换到`uwsgi`设定的`uid` `gid`用户。

* mongoengine connect

mongodb多进程连接问题在文档 [Using PyMongo with Multiprocessing](http://api.mongodb.com/python/current/faq.html#using-pymongo-with-multiprocessing) 中描述了pymongo对于多进程连接的解决方案：pymongo 设置connect参数`connect=False`,或者在fork之后再连接。

[pymongo connect api](http://api.mongodb.com/python/current/api/pymongo/mongo_client.html)文档说明

```
connect (optional): if True (the default), immediately begin connecting to MongoDB in the background. Otherwise connect on the first operation.
```

因此`djnago settings.py`文件配置为`mongoengine.connect(_MONGODB_NAME, host=_MONGODB_HOST, port=_MONGODB_PORT, connect=False)`

* supervisor log

supervisord.conf 文件中配置`.log`和`.sock`的文件目录，执行supervisord的用户必须有读写的权限，参考方式为：`chown -R user/user /data/log`.