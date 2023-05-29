from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Blog

User = get_user_model()

class BlogTests(APITestCase):
    def setUp(self):
        user = User.objects.create(email='test@email.com',username='test')

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        self.refresh_token = str(refresh_token)
        self.access_token= str(access_token)


        url = reverse('create_blog')
        data = {
            'name':'test blog',
            'description':'this is the description for the test blog'
        }
        headers = {
            'Authorization':f'Bearer {self.access_token}'
        }
        self.client.post(url,data,headers=headers)
        self.blog = Blog.objects.first()

    def test_create_blog(self):
        url = reverse('create_blog')
        data = {
            'name':'test2 blog',
            'description':'this is the description for the test blog'
        }
        headers = {
            'Authorization':f'Bearer {self.access_token}'
        }
        client = self.client.post(url,data,headers=headers)
        blog = Blog.objects.get(name='test2 blog')

        self.assertEqual(client.status_code, status.HTTP_201_CREATED)
        self.assertEqual(blog.name,'test2 blog')
        self.assertEqual(blog.description,'this is the description for the test blog')
        self.assertEqual(blog.owner.email,'test@email.com')

        # test if I can create another blog with the same name
        client = self.client.post(url, data, headers=headers)

        self.assertEqual(client.status_code, status.HTTP_400_BAD_REQUEST)

        blogs_count = Blog.objects.all().count()
        self.assertEqual(blogs_count, 2)
        
    def test_update_blog(self):
        # first creating a blog

        # Now I have a blog I will make a logic for testing the permissions and then I will test the edit blog view
        # I will create this user to test if the permission is work like I expected or not

        new_user = User.objects.create(email='test2@email.com')
        refresh_token = RefreshToken.for_user(new_user)
        access_token = str(refresh_token.access_token)

        url = reverse('update_blog')
        data = {
            'name':'Edited blog',
            'description':'This is the edited description for the test blog',
            'blog_id':self.blog.id
        }
        headers = {
            'Authorization':f'Bearer {access_token}'
        }
        # This client uses the new user's access token so the result will be 403 status code
        client = self.client.put(url, data, headers=headers)
        self.assertEqual(client.status_code, status.HTTP_403_FORBIDDEN)
        
        # This client uses the access token of the user that I created above so it will be good
        headers = {
            'Authorization':f'Bearer {self.access_token}'
        }
        client = self.client.put(url,data,headers=headers)

        self.assertEqual(client.status_code, status.HTTP_200_OK)

        edited_blog = Blog.objects.first()
        self.assertEqual(edited_blog.name, 'Edited blog')
        self.assertEqual(edited_blog.description, 'This is the edited description for the test blog')

    def test_delete_blog(self):
        url = reverse('delete_blog')
        data = {
            'blog_id':self.blog.id
        }

        new_user = User.objects.create(email='test2@email.com')
        refresh_token = RefreshToken.for_user(new_user)
        access_token = str(refresh_token.access_token)

        headers = {
            'Authorization':f'Bearer {access_token}'
        }

        client = self.client.delete(url,data,headers=headers)
        blogs_count = Blog.objects.all().count()

        self.assertEqual(client.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(blogs_count, 1)

        # Now I will test the proccess of deletion with the real user
        
        headers = {
            'Authorization':f'Bearer {self.access_token}'
        }

        client = self.client.delete(url,data,headers=headers)
        blogs_count = Blog.objects.all().count()

        self.assertEqual(client.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(blogs_count, 0)
