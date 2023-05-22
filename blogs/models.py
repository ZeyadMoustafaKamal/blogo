from django.db import models
from accounts.models import CustomUser
import uuid


class Blog(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )

    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='owner')
    members = models.ManyToManyField(CustomUser)
    
    name = models.CharField(max_length=75,unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(default='blog-default.png', upload_to='media/blog_images')

    def __str__(self):
        return self.name
  
class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True,
                          editable=False
                          )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser,unique=False, on_delete=models.CASCADE, related_name='reciever')

    body = models.CharField(max_length=150)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=250, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f'form {self.sender} , to : {self.reciever}'
