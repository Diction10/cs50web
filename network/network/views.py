from django import http
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    # Query db for all posts
    posts = Post.objects.all().order_by('-date_posted')
    # paginator show 10 per page
    paginator = Paginator(posts, 10) # Show 10 posts per page.
    
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    return render (request, 'network/index.html', {
        'posts': posts,
        'page_obj': page_obj
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='login')
def new_post(request):
    form = NewPostForm()
    
    if request.method == 'POST':
        # ensure user is authenticated
        if request.user.is_authenticated:
            
            post = NewPostForm(request.POST)

            # Check if form is valid
            if post.is_valid():
                # save to database
                obj = post.save(commit=False)
                obj.user = request.user
                obj.save()
                
                # after submission redirect to the home page
                return HttpResponseRedirect(reverse("index"))

    return render(request, "network/post.html", {
        'form' : form
    })


# define function all_post
@login_required(login_url='login')
@csrf_exempt
def all_posts(request):
    # Query db for all posts
    posts = Post.objects.all().order_by('-date_posted')
    # paginator show 10 per page
    paginator = Paginator(posts, 10) # Show 10 posts per page.
    
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    return render (request, 'network/all_post.html', {
        'posts': posts,
        'page_obj': page_obj
    })


# profile page
@login_required(login_url='login')
@csrf_exempt
def profile (request, user):
    
    # Query database for user's profile
    u_profile = User.objects.get(username=user)

    posts = Post.objects.filter(user=u_profile.id).order_by('-date_posted')

    # paginator show 10 per page
    paginator = Paginator(posts, 10) # Show 10 posts per page.
    
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)
   
    return render (request, 'network/profile.html', {
        'profil': u_profile,
        'page_obj': page_obj,
        'posts': posts,
    })
    

# define the following post function
@login_required(login_url='login')
def following_posts(request):
    # lists of posts
    posts = []

    post_contents = []

    # Query db for list of users current user follows
    curr_user_following = Profile.objects.filter(followers=request.user)

    for following in curr_user_following:
        # get the post profile of all the listed users
        p = Post.objects.filter(user=following.user_id).order_by('-date_posted')
        # add the post profile to the empty post list
        posts.append(p)
    
    # iterate through the post to turn the list into a single list
    for post in posts:
        for d in post:
            post_contents.append(d)  
    
    paginator = Paginator(post_contents, 10) # Show 10 posts per page.
    
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    return render (request, 'network/following.html', {
        'posts': post_contents,
        'page_obj': page_obj
    })

# API request for follow or unfollow users
@login_required(login_url='login')
@csrf_exempt
def users(request, user):
    # Query database for user's profile
    u_profile = User.objects.get(username=user)

    user_profile = u_profile.profile    

    json_profile = serializers.serialize("json", [user_profile])
    d = json.loads(json_profile)

    if request.method == 'PUT':
        curr_profile = User.objects.get(username=request.user)
        curr_user = curr_profile.profile

        data = json.loads(request.body)

        if data.get('is_following') is True:
            # set the current user to follow the profile owner
            curr_user.following.add(data.get('following'))

            # set the profile owner to be followed by current user
            user_profile.followers.add(curr_profile.id)
            user_profile.is_following = data.get('is_following')
        else:
            # remove profile from both following and follows
            curr_user.following.remove(data.get('following'))
            user_profile.followers.remove(curr_profile.id)
            user_profile.is_following = data.get('is_following')

        # save to database
        user_profile.save()
        curr_user.save()

        return HttpResponse(status=204)

    # if request.method == 'PUT':
    return JsonResponse(d, safe=False)

# function to edit post
@login_required(login_url='login')
@csrf_exempt
def edit_post(request, user, post_id):    

    # make sure user cannot edit other user's post
    if str(request.user) != user:
        return HttpResponse('You do not have Authorization to edit this post!!!')

    # query db for user's post
    post = Post.objects.get( pk=post_id)

    # convert post object to json string
    json_post = serializers.serialize("json", [post])
    d = json.loads(json_post)
    
    # API to edit post
    if request.method == 'POST':
        # get jsonify of edited post
        d = json.loads(request.body)
        # set edited content to new content
        post.post_content = d.get('edited_post')
        # save to daatabase
        post.save()
        return redirect('profile', user=request.user)

    elif request.method == 'PUT':
        like = json.loads(request.body)
        if like.get("has_liked") is True:
            # set the current post to be liked by the current user
            post.user_like.add(like.get('user_like'))
        else:
            # remove the current post from being liked by the current user
            post.user_like.remove(like.get('user_like'))

        # ave to database
        post.save() 
        return HttpResponse(status=204)

    # API get method returns this
    return JsonResponse(d, safe=False)



# API to load like and unlike
@csrf_exempt
def like(request, user):
    user = User.objects.get(username=request.user)
    # create an empty list to store post(s) user has liked
    post_liked = []

    # get all the post that the user has liked
    liked_post = user.liked.all()

    # add the posts liked by the user to the empty list
    for post in liked_post:
        post_liked.append(post.id)

    # convert list to string
    d = json.dumps(post_liked)
    # load the string
    f = json.loads(d)

    # API get method returns this
    return JsonResponse(f, safe=False)
        
    
    

        
   