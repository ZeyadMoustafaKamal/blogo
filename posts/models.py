from django.db import models
from accounts.models import CustomUser
from blogs.models import Blog

class Post(models.Model):
    
    auther = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.auther.username} , {self.title}'

class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    content = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'user : {self.author} , content : {self.content}'
