from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Post, Comment
from .serializers import ListPostsSerializer, CreatePostSerializer, EditPostSerializer, CreateCommentSerializer,ListCommentSerializer,EditCommentSerializer
from .permissions import IsCommentAuthor

from blogs.permissions import CanManagePosts

# Posts management

class ListPostsView(ListAPIView):

    authentication_classes = ()
    permission_classes = ()
    queryset = Post.objects.all()

    serializer_class = ListPostsSerializer
    pagination_class = PageNumberPagination

    pagination_class.page_size = 20

class RetrievePostView(RetrieveAPIView):
    serializer_class = ListPostsSerializer
    def get_object(self):
        post_id = self.request.data.get('post_id')
        return get_object_or_404(Post, id=post_id)

class CreatePostView(CreateAPIView):
    serializer_class = CreatePostSerializer
    permission_classes = IsAuthenticated,CanManagePosts

class EditPostView(UpdateAPIView):
    serializer_class = EditPostSerializer
    permission_classes = IsAuthenticated,CanManagePosts
    def get_object(self):
        post_id = self.request.data.get('post_id')
        return get_object_or_404(Post, id=post_id)

class DeletePostView(DestroyAPIView):
    permission_classes = IsAuthenticated,CanManagePosts
    def get_object(self):
        post_id = self.request.data.get('post_id')
        post = get_object_or_404(Post,id=post_id)
        return post

# Comments management

class CreateCommentView(CreateAPIView):
    serializer_class = CreateCommentSerializer

class ListCommentsView(ListAPIView):
    serializer_class = ListCommentSerializer

    authentication_classes = ()
    permission_classes = ()

    pagination_class = PageNumberPagination
    pagination_class.page_size = 25

    def get_queryset(self):
        post_id = self.request.data.get('post')
        post = get_object_or_404(Post, id=post_id)
        queryset = Comment.objects.filter(post=post)
        return queryset

class DeleteCommentView(DestroyAPIView):
    permission_classes  = IsAuthenticated,IsCommentAuthor
    def get_object(self):
        comment_id = self.request.data.get('comment')
        comment = get_object_or_404(Comment, id=comment_id)
        self.check_object_permissions(self.request,comment)
        return comment

class EditCommentsView(UpdateAPIView):
    serializer_class = EditCommentSerializer
    permission_classes = IsAuthenticated,IsCommentAuthor
    def get_object(self):
        comment_id = self.request.data.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        self.check_object_permissions(self.request, comment)
        return comment


