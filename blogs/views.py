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
        member_blogs = request.user.blog_set.exclude(owner=request.user)

        data = {
            'owner_blogs'  : self.serializer_class(owner_blogs,many=True).data,
            'member_blogs' : self.serializer_class(member_blogs,many=True).data
        }

        return Response(data)

class CreateBlogView(CreateAPIView):
    serializer_class = CreateBlogSerializer

class BlogDetailsView(RetrieveAPIView):
    serializer_class = BlogDetailsSerializer
    permission_classes = ()
    authentication_classes = ()
    def get_object(self):
        blog = get_object_or_404(Blog, id=self.request.data.get('id'))
        return blog

class UpdateBlogView(UpdateAPIView):
    serializer_class = UpdateBlogSerializer
    permission_classes = IsAuthenticated,CanManageBlog
    def get_object(self):
        blog = get_object_or_404(Blog,id=self.request.data.get('id'))
        return blog

class DeleteBlogView(DestroyAPIView):
    permission_classes = IsAuthenticated,CanManageBlog
    def get_object(self):
        blog_id = self.request.data.get('id')
        return get_object_or_404(Blog,id=blog_id)

class InviteMembersView(CreateAPIView):

    serializer_class = InviteMemberSerializer
    permission_classes = IsAuthenticated,CanManageMembers

