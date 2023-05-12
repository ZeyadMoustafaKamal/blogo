from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('blogs/',include('blogs.urls')),
    path('__debug__/',include('debug_toolbar.urls'))
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)