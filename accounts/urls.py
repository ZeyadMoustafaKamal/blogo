from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from . import views

urlpatterns = [

    path('signup/', views.SignUpView.as_view() , name='signup'),
    path('notifications/', views.ListNotificationsView.as_view(), name='notifications'),
    path('update/',views.UpdateUserInfoView.as_view(),name='update_user_info'),
    path('notifications/update/',views.UpdateNotificationView.as_view(), name='update_notification'),


    # JWT obtain and refresh token

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
]
