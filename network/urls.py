
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="newpost"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow/<int:user_follow>", views.follow, name="follow"),
    path("unfollow/<int:user_unfollow>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("like/<int:post_id>", views.like, name="like"),
    path("unlike/<int:post_id>", views.unlike, name="unlike"),
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post")
]
