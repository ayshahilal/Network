from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, related_name="owner")
    comment = models.CharField(max_length = 256)
    date =  models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
   
    def __str__(self):
        return f"{self.owner}: {self.comment}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, related_name="follower")
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, related_name="followed_user")
    
    def __str__(self):
        return f"{self.user} is following {self.followed_user}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, related_name="liker")
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, blank = True, related_name="liked_post")
    
    def __str__(self):
        return f"{self.user} liked: '{self.liked_post}'"