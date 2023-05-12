from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .permissions import create_blog_permissions_and_groups
from .models import Blog, Notification

from accounts.serializers import UserSerializer
from posts.models import Post

User = get_user_model()

class BlogsSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)
    class Meta:
        model = Blog
        fields = '__all__'

class CreateBlogSerializer(serializers.ModelSerializer):

    owner = UserSerializer(read_only=True)
    members = serializers.PrimaryKeyRelatedField(read_only=True,many=True)

    class Meta:
        model = Blog
        fields = '__all__'
        extra_kwargs = {
            'image':{'required':False},
            'blog_code':{'required':False}
        }
    def create(self, validated_data):
        owner =  self.context['request'].user
        validated_data['owner'] = owner
        blog = Blog.objects.create(
            **validated_data
        )
        blog.members.add(owner)
        create_blog_permissions_and_groups(blog.id)
        owner_group = Group.objects.get(name=f'admin{blog.id}')
        owner.groups.add(owner_group)
        return blog

class BlogDetailsSerializer(serializers.Serializer):

    posts_count = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    name = serializers.CharField()
    description = serializers.CharField()
    owner = UserSerializer()
    created_at = serializers.DateTimeField()
    image = serializers.SerializerMethodField()

    def get_image(self,blog):
        return self.context.get('request').build_absolute_uri(blog.image.url)
    
    def get_posts_count(self,blog):
        return Post.objects.filter(blog=blog).count()
    
    def get_members(self,blog):
        members_queryset = blog.members.all()
        members_serilizer = UserSerializer(members_queryset,many=True)
        return members_serilizer.data

class UpdateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['name','description']
    
    def validate_name(self,value):

        if Blog.objects.filter(name=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError('This name is already taken')

        return value
    def update(self, instance, validated_data):
        
        instance.name = validated_data.get('name')
        instance.description = validated_data.get('description')
        instance.save()
        
        return instance

class InviteMemberSerializer(serializers.ModelSerializer):

    sender = UserSerializer(read_only=True)
    receiver = serializers.CharField(max_length=25)

    blog = serializers.UUIDField()

    class Meta:
        model = Notification
        fields = ['sender','receiver','body','blog','permissions']


    def validate_receiver(self,value):
        
        receiver = get_object_or_404(User,email=value)
        if not receiver:
            raise serializers.ValidationError('No User with this email')
        if Notification.objects.filter(receiver=receiver,is_read=False).exists():
            raise serializers.ValidationError('You sent an invitation for this user before')
        if self.context.get('request').user == receiver:
            raise serializers.ValidationError('You can\' send an invitaion for your self')
        return receiver
    
    
    def create(self, validated_data,*args, **kwargs):

        blog = get_object_or_404(Blog, id=self.validated_data.get('blog'))

        validated_data['blog'] = blog

        permissions = self.validated_data.get('permissions').split(',')

        permissions = [permission + str(blog.id) + ',' for permission in permissions]

        validated_data['permissions'] = ''.join(permissions)[:-1]

        validated_data['sender'] = self.context.get('request').user

        notification = Notification.objects.create(
            **validated_data)

        return notification
