from django.contrib import admin

from .models import Blog
from posts.models import Post

class PostInline(admin.StackedInline):
    model = Post

    fields = 'title', 'description',
    extra = 1

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fields = 'owner','name', 'description', 'image'
    list_display = 'name', 'description'
    list_display_links = 'name',
    search_fields = 'name', 'description'
    list_per_page = 25
    list_filter = 'created_at',
    inlines = [PostInline]
    
