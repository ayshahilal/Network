from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Follow, Like
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required


def index(request):
    all_posts = Post.objects.all().order_by("id").reverse()

    paginator = Paginator(all_posts, 10)
    current_page_number = request.GET.get('page')
    current_page = paginator.get_page(current_page_number)

    posts_liked_by_user = []

    if request.user.is_authenticated:
        liked_by_user = Like.objects.filter(user = request.user)
        for post in liked_by_user:
            posts_liked_by_user.append(post.liked_post.id)

    for post in all_posts:
        post = Post.objects.get(pk=post.id)
        count_like = Like.objects.filter(liked_post=post).count()
        post.likes = count_like
        post.save()

    return render(request, "network/index.html",{
        "current_page": current_page,
        "main_page": True,
        "posts_liked": posts_liked_by_user
    })

@login_required
def following(request):
    logedin_user = User.objects.get(pk=request.user.id)
    following_users = Follow.objects.filter(user=logedin_user)
    all_posts = Post.objects.all().order_by("id").reverse()
    posts = []
    posts_liked_by_user = []

    if request.user.is_authenticated:
        liked_by_user = Like.objects.filter(user = request.user)
        for post in liked_by_user:
            posts_liked_by_user.append(post.liked_post.id)

    for post in all_posts:
        for user in following_users:
            if user.followed_user == post.owner:
                posts.append(post)

    paginator = Paginator(posts, 10)
    current_page_number = request.GET.get('page')
    current_page = paginator.get_page(current_page_number)

    return render(request, "network/index.html",{
        "current_page": current_page,
        "main_page": False,
        "posts_liked": posts_liked_by_user
    })

@login_required
def follow(request, user_follow):
    if request.method == "POST":
        user = request.user
        user_to_follow = User.objects.get(pk=user_follow)
        follow_rel = Follow(user=user, followed_user=user_to_follow)
        follow_rel.save()
        return HttpResponseRedirect(reverse("profile", args=(user_follow,)))

@login_required
def unfollow(request, user_unfollow):
    if request.method == "POST":
        user = request.user
        user_to_unfollow = User.objects.get(pk=user_unfollow)
        Follow.objects.filter(user=user, followed_user=user_to_unfollow).delete()
        return HttpResponseRedirect(reverse("profile", args=(user_unfollow,)))

@login_required
def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like(user=user, liked_post=post)
    like.save()
    count_like = Like.objects.filter(liked_post=post).count()
    return JsonResponse({"message":"success like","data":count_like})

@login_required
def unlike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user, liked_post=post)
    like.delete()
    count_like = Like.objects.filter(liked_post=post).count()
    return JsonResponse({"message":"success unlike","data":count_like})

def profile(request, user_id):
    user_profile = User.objects.get(pk=user_id)
    posts = Post.objects.filter(owner=user_profile).order_by("id").reverse()
    
    paginator = Paginator(posts, 10)
    current_page_number = request.GET.get('page')
    current_page = paginator.get_page(current_page_number)
    post_exists = True if current_page.object_list else False

    followers = Follow.objects.filter(followed_user=user_profile)
    followings = Follow.objects.filter(user=user_profile)
    
    isFollowing = False
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user, followed_user=user_profile).exists():
            isFollowing = True

    posts_liked_by_user = []

    if request.user.is_authenticated:
        liked_by_user = Like.objects.filter(user = request.user)
        for post in liked_by_user:
            posts_liked_by_user.append(post.liked_post.id)

    profile_data =  {
        "current_page": current_page,
        "username": user_profile.username,
        "user_profile": user_profile,
        "followers":  followers,
        "followers_count": followers.count,
        "followings": followings,
        "followings_count": followings.count,
        "post_exists": post_exists,
        "isFollowing": isFollowing,
        "posts_liked": posts_liked_by_user
    }

    return render(request, "network/profile.html", profile_data)

@login_required
def edit_post(request, post_id):
    if request.method == "POST":
        new_comment = json.loads(request.body)
        changedPost = Post.objects.get(pk=post_id)
        changedPost.comment = new_comment["new_content"]
        changedPost.save()
        return JsonResponse({"message":"success","data": new_comment["new_content"]})
    
@login_required
def new_post(request):
    if request.method == "POST":
        user = request.user
        comment = request.POST['comment']
        newPost = Post(owner=user, comment=comment)
        newPost.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def delete_post(request, post_id):
    if request.method == "POST":
        deletePost = Post.objects.get(pk=post_id)
        deletePost.delete()
        return HttpResponseRedirect(reverse("profile", args=(request.user.id,)))
    
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


@login_required
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
