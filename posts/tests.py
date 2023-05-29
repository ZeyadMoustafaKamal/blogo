from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.urls import reverse

from blogs.models import Blog
from .models import Post, Comment

User = get_user_model()

class PostTests(APITestCase):
    def setUp(self):
        user = User.objects.create(email='test@email.com')
        # I will use the test_user to test my permissions
        test_user = User.objects.create(email='test2@email.com',username='test user')
        test_user_refresh_token = RefreshToken.for_user(test_user)
        self.test_user_access_token = str(test_user_refresh_token.access_token)

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        self.access_token = str(access_token)

        create_blog_url = reverse('create_blog')
        data = {
            'name':'test blog',
            'description':'this is my test blog'
        }
        headers = {
            'Authorization':f'Bearer {self.access_token}'
        }

        client = self.client.post(create_blog_url,data,headers=headers)
        self.assertEqual(client.status_code, status.HTTP_201_CREATED)

        self.blog = Blog.objects.first()

        # Now I will create a post

        create_post_url = reverse('create_post')
        data = {
            'blog_id':self.blog.id,
            'title':'test post',
            'description':'this is the test post'
        }
        headers = {
            'Authorization':f'Bearer {self.access_token}'
        }

        client = self.client.post(create_post_url,data,headers=headers)
        self.assertEqual(client.status_code, status.HTTP_201_CREATED)

        self.post = Post.objects.get(title='test post')

    def test_create_post(self):
        url = reverse('create_post')
        data = {
            'blog_id':self.blog.id,
            'title':'test2 post',
            'description':'this is the test2 post'
        }
        headers = {}
        # This user shouldn't have the permissions to create a post in this blog



        headers['Authorization'] = f'Bearer {str(self.test_user_access_token)}'

        client = self.client.post(url,data,headers=headers)

        self.assertEqual(client.status_code,status.HTTP_403_FORBIDDEN)

        headers['Authorization'] = f'Bearer {self.access_token}'

        client = self.client.post(url,data,headers=headers)
        post = Post.objects.get(title='test2 post')
        posts_count = Post.objects.all().count()

        self.assertEqual(client.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.title, 'test2 post')
        self.assertEqual(post.description, 'this is the test2 post')
        self.assertEqual(posts_count, 2)

    def test_edit_post(self):
        url = reverse('edit_post')
        data = {
            'title':'Edited post',
            'description':'This is the edited post',
            'post_id':self.post.id
        }
        headers = {}
        headers['Authorization'] = f'Bearer {self.test_user_access_token}'

        client = self.client.put(url, data, headers=headers)
        post_is_edited_or_not = Post.objects.filter(title='Edited post').exists()

        self.assertEqual(client.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(post_is_edited_or_not)

        headers['Authorization'] = f'Bearer {self.access_token}'
        client = self.client.put(url,data, headers=headers)
        post_is_edited_or_not = Post.objects.filter(title='Edited post').exists()

        self.assertEqual(client.status_code, status.HTTP_200_OK)
        self.assertTrue(post_is_edited_or_not)

    def test_delete_post(self):
        url = reverse('delete_post')
        data = {
            'post_id':self.post.id
        }
        headers = {}
        headers['Authorization'] = f'Bearer {self.test_user_access_token}'
        client = self.client.delete(url,data,headers=headers)
        self.assertEqual(client.status_code, status.HTTP_403_FORBIDDEN)

        headers['Authorization'] = f'Bearer {self.access_token}'
        client = self.client.delete(url,data,headers=headers)
        posts_count = Post.objects.all().count()

        self.assertEqual(client.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(posts_count, 0)

class CommentTest(APITestCase):
    def setUp(self):
        user = User.objects.create(email='test@email.com')
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        self.access_token = str(access_token)


        # I will use the test_user to test my permissions
        test_user = User.objects.create(email='test2@email.com',username='test user')
        test_user_refresh_token = RefreshToken.for_user(test_user)
        self.test_user_access_token = str(test_user_refresh_token.access_token)

        create_blog_url = reverse('create_blog')
        data = {
            'name':'test blog',
            'description':'this is my test blog'
        }
        headers = {
            'Authorization':f'Bearer {self.access_token}'
        }

        client = self.client.post(create_blog_url,data,headers=headers)
        self.assertEqual(client.status_code, status.HTTP_201_CREATED)

        self.blog = Blog.objects.first()

        # Now I will create a post

        create_post_url = reverse('create_post')
        data = {
            'blog_id':self.blog.id,
            'title':'test post',
            'description':'this is the test post'
        }
        headers = {
            'Authorization':f'Bearer {self.access_token}'
        }

        client = self.client.post(create_post_url,data,headers=headers)
        print(client.json())
        self.assertEqual(client.status_code, status.HTTP_201_CREATED)

        self.post = Post.objects.get(title='test post')

        create_comment_url = reverse('create_comment')
        data = {
            'post_id':self.post.id,
            'content':'test comment',
        }
        headers = {
            'Authorization':f'Bearer {self.access_token}'
        }

        client = self.client.post(create_comment_url,data,headers=headers)
        self.assertEqual(client.status_code, status.HTTP_201_CREATED)

        self.comment = Comment.objects.get(content='test comment')

    def test_create_comment(self):
        url = reverse('create_comment')
        data = {
            'content':'my test comment',
            'post_id':self.post.id
        }
        headers = {}
        headers['Authorization'] = f'Bearer {self.access_token}'

        client = self.client.post(url, data, headers=headers)
        comment = Comment.objects.get(content='my test comment')
        comments_count = Comment.objects.all().count()

        self.assertEqual(client.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment.content, 'my test comment')
        self.assertEqual(comments_count, 2)

    def test_edit_comment(self):
        url = reverse('edit_comment')
        data = {
            'content':'my edited test comment',
            'comment_id':self.comment.id
        }
        headers = {}
        headers['Authorization'] = f'Bearer {self.test_user_access_token}'

        client = self.client.put(url, data, headers=headers)
        edited_or_not = Comment.objects.filter(content='my edited test comment').exists()

        self.assertEqual(client.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(edited_or_not)

        headers['Authorization'] = f'Bearer {self.access_token}'

        client = self.client.put(url, data, headers=headers)
        edited_or_not = Comment.objects.filter(content='my edited test comment').exists()

        self.assertEqual(client.status_code, status.HTTP_200_OK)
        self.assertTrue(edited_or_not)

    def test_delete_comment(self):
        url = reverse('delete_comment')
        data = {
            'comment_id':self.comment.id
        }
        headers = {}
        headers['Authorization'] = f'Bearer {self.test_user_access_token}'

        client = self.client.delete(url, data, headers=headers)
        comments_count = Comment.objects.all().count()

        self.assertEqual(client.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(comments_count, 1)

        
        headers['Authorization'] = f'Bearer {self.access_token}'

        client = self.client.delete(url, data, headers=headers)
        comments_count = Comment.objects.all().count()

        self.assertEqual(client.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(comments_count, 0)