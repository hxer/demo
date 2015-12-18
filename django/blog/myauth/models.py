from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings

import os.path

"""Fix
[1] function get_picture use http://...,
    change it for you need
"""
class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=50, null=True, blank=True)

    def get_url(self):
        return "http://"+str(self.url) if "http://" not in self.url and \
            "https://" not in self.url else self.url

    def get_picture(self):
        no_picture = "https://github.com/hxer/personal/blob/master/simple.jpg"
        try:
            filename = os.path.join(settings.MEDIA_ROOT, 'profile_pictures') + \
                self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' + \
                self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            elif os.path.isfile(settings.MEDIA_ROOT+'simple.jpg'):
                print(settings.MEDIA_ROOT, settings.MEDIA_URL)
                return settings.MEDIA_URL + 'simple.jpg'
        except:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
