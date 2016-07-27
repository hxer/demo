from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Post
import datetime

# Create your views here.
def home(request):
    # get all post form DB
    posts = Post.objects
    return render(request, 'demo/index.html', {"posts": posts})

def detail(request, id):
    # query by id
    post = Post.objects(id=id)[0]
    return render(request, 'demo/post.html', {"post": post})
    
def create(request):
    if request.method == "POST":
        # fetch data from post data
        title = request.POST['title']
        content = request.POST['content']
        update_time = datetime.datetime.now()

        # not check data security or valid
        post = Post(title=title, content=content, last_update=update_time)
        post.save()
        return redirect('home') 

    return render(request, 'demo/create.html')

def update(request, id):
    post = Post.objects(id=id)[0]
    
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        update_time = datetime.datetime.now()
        
        # update
        post.title = title
        post.content = content
        post.last_update = update_time
        post.save()
        return redirect('home') 

    return render(request, 'demo/update.html', {'post': post})

def delete(request, id):
    post = Post.objects(id=id)[0]
    post.delete()
    return redirect('home')