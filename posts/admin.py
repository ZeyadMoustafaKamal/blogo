from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(blog__members=request.user)
        return qs
    fields = 'auther', 'blog', 'title', 'description'
    search_fields = 'title', 'description'
    list_display = 'title', 'description', 'created_at', 'num_of_comments'
    inlines = [CommentInline]

    def num_of_comments(self, obj):
        return obj.comment_set.count()
