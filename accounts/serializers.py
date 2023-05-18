from rest_framework import serializers

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Permission

from blogs.models import Notification


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'username','email','date_joined'

class NotificationsSerializer(serializers.ModelSerializer):
    from blogs.serializers import BlogsSerializer

    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    blog = BlogsSerializer(read_only=True)

    

    class Meta:
        model = Notification
        fields = 'id', 'sender', 'receiver', 'body', 'blog', 'permissions', 'timestamp', 'is_read'


class UpdateNotificationSerializer(serializers.ModelSerializer):

    choice = serializers.BooleanField(required=False)
    class Meta:
        model = Notification
        fields = 'notification_id','choice'

    def update(self, instance, validated_data):

        receiver = self.context['request'].user
        choice = validated_data.get('choice')
        # the choice can be true or false or nothing so If it was true just the user will be added to the members and all 
        # of the related operations will be excuted and if it something else I will just mark the Notifications as (read)
        if choice:
            instance.is_read = True
            permissions_codenames = instance.permissions.split(',')
            instance.blog.members.add(receiver)
            for codename in permissions_codenames:
                
                permission = Permission.objects.get(codename=codename)
                receiver.user_permissions.add(permission)     
        else:
            instance.is_read = True

        return super().update(instance, validated_data)



class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=35)
    password2 = serializers.CharField(max_length=35, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate_password2(self, value):
        password1 = self.get_initial().get('password', '')
        if password1 != value:
            raise serializers.ValidationError('Two passwords must match')
        if len(value.strip()) < 8:
            raise serializers.ValidationError('The password must be at least 8 characters long')
        return value

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError('There is a user with this email')
        if User.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError('The username is already taken')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'user_code']
    def validate(self, attrs):
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError('incorrect email or password')
        return attrs
    
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'username',
    def validate_username(self,value):

        current_user_username= self.context.get('request').user.username

        if User.objects.filter(username=value).exclude(username=current_user_username).exists():
            raise serializers.ValidationError('The username us already taken')
        
        return value
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username')
        instance.save()
        return instance

