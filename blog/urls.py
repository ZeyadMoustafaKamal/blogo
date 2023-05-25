from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="This is my API documenation and in this one you will be able to know alot about my API and the endpoints of it and how to deal with it",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
    path('admin/', admin.site.urls),
    path('blogs/',include('blogs.urls')),
    path('__debug__/',include('debug_toolbar.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)