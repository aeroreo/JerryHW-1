from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
from .models import Post
from . import models
import datetime


# Create your views here.
def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_page(request):
	return render_to_response('blog/post_new.html')

def edit_page(request):
	try:
		pid=request.GET["id"]
		posts = Post.objects.filter(p_id = pid)
		return render(request, 'blog/post_edit.html', {'posts': posts})
	except:
		return HttpResponseRedirect('/blog/')

def view(request):
	try:
		pid=request.GET["id"]
		posts = Post.objects.filter(p_id = pid)
		title= ""

		for post in posts:
			title = post.title

		return render(request, 'blog/post_view.html', {'posts': posts, 'title': title})
	except:
		return HttpResponseRedirect('/blog/')
		

def save(request):
    user = request.POST.get("tb_user")
    ti = request.POST.get("tb_title")
    tx = request.POST.get("tb_text")
    created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    publish = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    n_post = models.Post(author = user, title = ti, text = tx, created_date = created, published_date = publish)
    n_post.save()

    return HttpResponseRedirect('/blog/')

def update(request):
    try:
        pi = request.POST.get("tb_pid")
        thePost = Post.objects.get(p_id=pi)
        thePost.author = request.POST.get("tb_user")
        thePost.title = request.POST.get("tb_title")
        thePost.text = request.POST.get("tb_text")
        thePost.published_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        thePost.save()
        return HttpResponseRedirect('/blog/')
    except Exception as e:
         return HttpResponseRedirect('/blog/')


def delete(request):
    un = request.GET["id"]
    
    try:
        post = Post.objects.get(p_id=un)
        post.delete()
        return HttpResponseRedirect('/blog/')
    except:
         return HttpResponseRedirect('/blog/')