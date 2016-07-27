from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^detail/(?P<id>[\da-f]+)', views.detail, name='detail'),
    url(r'^create/', views.create, name='create'),
    url(r'^update/(?P<id>[\da-f]+)', views.update, name='update'),
    url(r'^delete/(?P<id>[\da-f]+)', views.delete, name='delete'),
]
