from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from core.forms import ProfileForm, ChangePasswordForm

import os
from PIL import Image

def home(request):
    if request.user.is_authenticated():
        return render(request, 'core/index.html')
    else:
        return render(request, 'core/cover.html')

@login_required
def setting(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.profile.url = form.cleaned_data.get('url')
            user.profile.location = form.cleaned_data.get('location')
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your profile were successfully edited.')
    else:
        form = ProfileForm(
            instance=user,
            initial={
                'url': user.profile.url,
                'location': user.profile.location
            }
        )
    return render(request, 'core/setting.html', {'form':form})

@login_required
def picture(request):
    upload_picture = True if request.GET.get('upload_picture')=='uploaded' else False
    return render(request, 'core/picture.html', {'upload_picture': upload_picture})

@login_required
def upload_picture(request):
    """
    Todo:
        文件类型或文件名过滤
    """
    try:
        if request.method == 'POST':
            profile_picture = os.path.join(settings.MEDIA_ROOT, 'profile_pictures/')
            if not os.path.exists(profile_pictures):
                os.mkdirs(profile_pictures)
            imgfile = request.FILE['picture']
            filename = profile_pictures + request.user.username + "_tmp.jpg"
            with open(filename, "wb+") as f:
                for chunk in imgfile.chunks():
                    f.write(chunk)
            im = Image.open(filename)
            width, height im.size
            if width > 350:
                new_width = 350
                new_height = (height*350)/width
                new_size = new_width, new_height
                im.thumbnail(new_size, Image.ANTIALIAS)
                im.save(filename)
            return redirect('/setting/picture/?upload_picture=uploaded')
        else:
            return redirect('/setting/picture/')
    except:
        return redirect('/setting/picture/')

@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = os.path.join(settings.MEDIA_ROOT, 'profile_pictures/') + \
            request.user.username + '_tmp.jpg'
        filename = os.path.join(settings.MEDIA_ROOT, 'profile_pictures/') + \
            request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop(x, y, w+x, w+y)
        cropped_im.thumbnail((200,200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)
    except:
        pass
    return redirect('/setting/picture/')

@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user.password = form.cleaned_data.get('new_password')
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your password were successfully changed')
    else:
        form = ChangePasswordForm(instance=user)
    return render(request, 'core/password.html', {'form':form})

@login_required
def profile(request, username):
    page_user = get_object_or_404(User, username=username)
    return render(request, 'core/profile.html',{'page_user':page_user,'page':1})
