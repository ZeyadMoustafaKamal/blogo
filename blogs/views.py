from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.generics import (CreateAPIView, 
                                    UpdateAPIView,
                                    ListAPIView, 
                                    RetrieveAPIView,
                                    DestroyAPIView
                                    )
from rest_framework.permissions import IsAuthenticated

from .models import Blog
from .permissions import (CanManageBlog, CanManageMembers)
from .serializers import (BlogsSerializer,
                        CreateBlogSerializer, 
                        BlogDetailsSerializer,
                        UpdateBlogSerializer, 
                        InviteMemberSerializer
                        )


class ListBlogsView(ListAPIView):

    serializer_class = BlogsSerializer

    def get(self,request,*args, **kwargs):
        owner_blogs = Blog.objects.filter(owner=request.user).all()
        owner_blogs_data = self.serializer_class(owner_blogs,many=True).data

        member_blogs = request.user.blog_set.exclude(owner=request.user)
        member_blogs_data = self.serializer_class(member_blogs,many=True).data

        data = {
            'owner_blogs'  : owner_blogs_data,
            'member_blogs' : member_blogs_data
        }

        return Response(data)

class CreateBlogView(CreateAPIView):
    serializer_class = CreateBlogSerializer

class BlogDetailsView(RetrieveAPIView):
    serializer_class = BlogDetailsSerializer
    permission_classes = ()
    authentication_classes = ()
    def get_object(self):
        blog = get_object_or_404(Blog, id=self.request.data.get('blog_id'))
        return blog

class UpdateBlogView(UpdateAPIView):
    serializer_class = UpdateBlogSerializer
    permission_classes = IsAuthenticated,CanManageBlog
    def get_object(self):
        blog_id = self.request.data.get('blog_id')
        blog = get_object_or_404(Blog,id=blog_id)
        self.check_object_permissions(self.request, blog)
        return blog

class DeleteBlogView(DestroyAPIView):
    permission_classes = IsAuthenticated,CanManageBlog
    def get_object(self):
        blog_id = self.request.data.get('blog_id')
        blog = get_object_or_404(Blog,id=blog_id)
        self.check_object_permissions(self.request, blog)
        return blog


class InviteMembersView(CreateAPIView):

    serializer_class = InviteMemberSerializer
    permission_classes = IsAuthenticated,CanManageMembers

