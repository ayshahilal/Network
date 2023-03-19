from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Follow, Like


class NetworkTests(TestCase):

    def setUp(self):
        # create users
        self.user1 = User.objects.create_user(
            username='user1', email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(
            username='user2', email='user2@example.com', password='password')
        self.user3 = User.objects.create_user(
            username='user3', email='user3@example.com', password='password')

        # create posts
        self.post1 = Post.objects.create(owner=self.user1, comment='Post 1')
        self.post2 = Post.objects.create(owner=self.user2, comment='Post 2')
        self.post3 = Post.objects.create(owner=self.user3, comment='Post 3')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['current_page'].object_list,
                                 ['<Post: user3: Post 3>', '<Post: user2: Post 2>', '<Post: user1: Post 1>'])

    def test_follow_view(self):
        # log in user1
        self.client.force_login(self.user1)

        # follow user2
        response = self.client.post(reverse('follow', args=[self.user2.id]))
        self.assertEqual(response.status_code, 302)

        # check that user1 is following user2
        self.assertTrue(Follow.objects.filter(
            user=self.user1, followed_user=self.user2).exists())

    def test_unfollow_view(self):
        # log in user1
        self.client.force_login(self.user1)

        # follow user2
        follow_rel = Follow.objects.create(
            user=self.user1, followed_user=self.user2)

        # unfollow user2
        response = self.client.post(reverse('unfollow', args=[self.user2.id]))
        self.assertEqual(response.status_code, 302)

        # check that user1 is not following user2
        self.assertFalse(Follow.objects.filter(
            user=self.user1, followed_user=self.user2).exists())

    def test_like_view(self):
        # log in user1
        self.client.force_login(self.user1)

        # like post2
        response = self.client.post(reverse('like', args=[self.post2.id]))
        self.assertEqual(response.status_code, 200)

        # check that user1 liked post2
        self.assertTrue(Like.objects.filter(
            user=self.user1, liked_post=self.post2).exists())

    def test_unlike_view(self):
        # log in user1
        self.client.force_login(self.user1)

        # like post2
        like = Like.objects.create(user=self.user1, liked_post=self.post2)

        # unlike post2
        response = self.client.post(reverse('unlike', args=[self.post2.id]))
        self.assertEqual(response.status_code, 200)

        # check that user1 unliked post2
        self.assertFalse(Like.objects.filter(
            user=self.user1, liked_post=self.post2).exists())
