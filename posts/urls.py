from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.ListPostsView.as_view(), name='all_posts'),
    path('get/',views.RetrievePostView.as_view(),name='get_post'),
    path('create/',views.CreatePostView.as_view(),name='create_post'),
    path('edit/',views.EditPostView.as_view(), name='edit_post'),
    path('delete/',views.DeletePostView.as_view(),name='delete_post'),

    path('comments/create/', views.CreateCommentView.as_view(), name='create_comment'),
    path('comments/list/', views.ListCommentsView.as_view(), name='list_comments'),
    path('comments/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('comments/edit/', views.EditCommentsView.as_view(), name='edit_comment')
]

