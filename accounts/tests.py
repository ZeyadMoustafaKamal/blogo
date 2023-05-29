from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AccountTests(APITestCase):
    def setUp(self):
        user = User.objects.create(username='test user',email='test2@email.com')
        user.set_password('12345678')
        user.save()

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        self.refresh_token = str(refresh_token)
        self.access_token = str(access_token)

    def test_create_account(self):
        url = reverse('signup')
        data = {
            'username':'test',
            'email':'test@email.com',
            'password':'asd11430',
            'password2':'asd11430'
        }
        client = self.client.post(url,data)

        account = User.objects.last()
        # the first user is the user that I created in setUp method

        self.assertEqual(client.status_code, status.HTTP_201_CREATED)
        self.assertEqual(account.username, 'test')
        self.assertContains(client,'refresh',status_code=status.HTTP_201_CREATED)
        self.assertContains(client,'access',status_code=status.HTTP_201_CREATED)


    def test_refresh_and_access(self):
        refresh_token_url = reverse('token_refresh')
        obtain_token_url = reverse('token_obtain_pair')

        # obtain_client tests
        obtain_client = self.client.post(obtain_token_url,{
            'email':'test2@email.com',
            'password':'12345678'
        })
        self.assertNotContains(obtain_client,'detail')
        self.assertEqual(obtain_client.status_code,status.HTTP_200_OK)
        self.assertContains(obtain_client,'refresh')
        self.assertContains(obtain_client,'access')

        # refresh_client tests
        refresh_token = obtain_client.json().get('refresh')
        refresh_client = self.client.post(refresh_token_url,{'refresh':refresh_token})

        self.assertEqual(refresh_client.status_code,status.HTTP_200_OK)
        self.assertContains(refresh_client,'refresh')
        self.assertContains(refresh_client,'access')

    def test_update_user_info(self):
        url = reverse('update_user_info')
        data = {'username':'edited_username'}
        headers = {'Authorization':f'Bearer {self.access_token}'}
        client = self.client.put(url, data, headers=headers)

        edited_user = User.objects.first()

        self.assertEqual(edited_user.username,'edited_username')
        self.assertEqual(client.status_code, status.HTTP_200_OK)