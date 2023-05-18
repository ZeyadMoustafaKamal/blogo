from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView,RetrieveAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import NotificationsSerializer, SignUpSerializer, UpdateNotificationSerializer, UpdateUserSerializer
from blogs.models import Notification
from .models import CustomUser


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    authentication_classes = ()
    permission_classes = ()
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(email=response.data.get('email'))
        refresh_token = RefreshToken.for_user(user)
        return Response({
            'refresh_token':str(refresh_token),
            'access_token':str(refresh_token.access_token)
        })

class UserInfoView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        # I think that I just need the username of the user but If I needed something else I will add it
        return Response({
            'username':request.user.username
        })

class UpdateUserInfoView(UpdateAPIView):
    serializer_class = UpdateUserSerializer
    def get_object(self):
        return self.request.user


class ListNotificationsView(ListAPIView):
    serializer_class = NotificationsSerializer

    def get_queryset(self):
        queryset = Notification.objects.filter(receiver=self.request.user)
        return queryset

class UpdateNotificationView(UpdateAPIView):

    serializer_class = UpdateNotificationSerializer

    def get_object(self):
        notification_id = self.request.data.get('notification_id')
        notification = get_object_or_404(Notification,id=notification_id)
        return notification

