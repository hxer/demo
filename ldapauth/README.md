# LDAP auth with django

## 认证

Django 自带一个用户认证系统，这个系统处理用户帐户、组、权限和基于 cookie 的 会话。

### 认证系统由以下部分组成：

* 用户
* 权限：控制用户进否可以执行某项任务的二进制（是/否）标志
* 组：一种为多个用户加上标签和权限的常用方式
* 消息：一种为指定用户生成简单消息队列的方式

[django 会话 用户登录](http://djangobook.py3k.cn/2.0/chapter14/)   
[django auth login view document](https://docs.djangoproject.com/en/1.8/topics/auth/default/#django.contrib.auth.views.login)


## 自定义身份验证

django可以自定义身份验证，Django 维护一个“认证后台”的列表。当调用django.contrib.auth.authenticate() 时, Django 会尝试所有的认证后台进行认证。如果第一个认证方法失败，Django 将尝试第二个，以此类推，直至试完所有的认证后台。

使用的认证后台通过AUTHENTICATION_BACKENDS 设置指定。它应该是一个包含Python 路径名称的元组，它们指向的Python 类知道如何进行验证。这些类可以位于Python 路径上任何地方。

默认情况下，AUTHENTICATION_BACKENDS 设置为：`('django.contrib.auth.backends.ModelBackend',)`.

`AUTHENTICATION_BACKENDS` 的顺序很重要，所以如果用户名和密码在多个后台中都是合法的，Django 将在第一个匹配成功后停止处理. 如果后台引发`PermissionDenied` 异常，认证将立即失败, Django 不会检查后面的认证后台。

### 编写一个认证后端¶

一个认证后端是个实现两个方法的类: `get_user(user_id)` 和 `authenticate(**credentials)`, `get_user` 方法要求一个参数 `user_id` –这个参数可以是用户名，数据库中的ID或其它标识 User 对象的主键, 方法返回一个 User 对象.

authenticate方法常用的关键参数如下：

```python
# username password
class MyBackend(object):
    def authenticate(self, username=None, password=None):
        # Check the username/password and return a User.
        ...

# token
class MyBackend(object):
    def authenticate(self, token=None):
        # Check the token and return a User.
        ...
```

authenticate 检查凭证, 如果凭证合法，返回一个匹配于登录信息的 User 实例。如果不合法，则返回 None.

## ldap

install on ubuntu

```
apt-get install libldap2-dev 
apt-get install libsasl2-dev
apt-get install python-ldap
```


## note

* `login_required()`

如果用户没有登录，那么就重定向到`settings.LOGIN_URL`, 并在查询字符串中传递当前绝对路径。例如：`/accounts/login/?next=/polls/3/` ;    
如果用户已登录，则正常的执行视图。视图代码认为用户已登录

`login_required()` 还有一个可选的 login_url 参数

```
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/') 
def my_view(request): 
    ... 
```

注意，如果你没有指定 `login_url` 参数，那么你需要为 settings.LOGIN_URL 映射适当的视图。例如，在缺省情况 下，在你的 URLconf 中加入以下一行:`(r'^accounts/login/$', 'django.contrib.auth.views.login')` 或者匹配你的登录视图映射到`accounts/longin/` url: `(r'^accounts/login/$', 'your_views.login')`

利用 `reverse()`函数灵活配置 `login_url`存在问题，`@login_required(login_url=reverse('login'))`这种用法会报错`The included urlconf 'ldapauth.urls' does not appear to have any patterns in it.`, 即`login_url`参数只能采用url硬编码的方式。 
