from django.urls import path

from . import views


urlpatterns = [
    path('all/', views.ListBlogsView.as_view(),name='all_blogs'),
    path('create/', views.CreateBlogView.as_view(),name='create_blog'),
    path('delete/',views.DeleteBlogView().as_view(), name='delete_blog'),
    path('details/', views.BlogDetailsView.as_view(),name='blog_details'),
    path('update/', views.UpdateBlogView.as_view(), name='update_blog'),
    path('invite/', views.InviteMembersView.as_view(), name='Invite'),
]
