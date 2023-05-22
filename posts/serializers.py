from rest_framework import serializers

from django.shortcuts import get_object_or_404

from .models import Post, Comment

from blogs.serializers import BlogsSerializer
from blogs.models import Blog
from accounts.serializers import UserSerializer

# posts management

class ListPostsSerializer(serializers.ModelSerializer):
    
    auther = UserSerializer()
    blog = BlogsSerializer()
    
    class Meta:
        model = Post
        fields = '__all__'

class CreatePostSerializer(serializers.ModelSerializer):
    auther = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['title','description','auther','blog']
        extra_kwargs = {
            'auther':{'required':False},
            'blog':{'source':'blog_id'}
        }
    
    def create(self, validated_data):
        auther = self.context['request'].user
        blog = get_object_or_404(Blog,id=self.context.get('request').data.get('blog_id'))
        validated_data['auther'] = auther
        validated_data['blog'] = blog
        post = Post.objects.create(
            **validated_data
        )
        return post

class EditPostSerializer(serializers.ModelSerializer):
    auther = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('title', 'description')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.description = validated_data.get('description')
        instance.save()
        return instance

# Comments management

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'post','content'
    def create(self, validated_data):

        author = self.context.get('request').user
        validated_data['author'] = author

        comment = Comment.objects.create(**validated_data)
        return comment

class ListCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    post = ListPostsSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

class EditCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'content',

