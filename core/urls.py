from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [

    path('api_schema/', get_schema_view(
        title='API Schema',
        description='Guide for the REST API',
        authentication_classes=(),
        permission_classes=()
    ), name='api_schema'),

    path('docs/', TemplateView.as_view(
        template_name='api_docs.html',
        extra_context={'schema_url':'api_schema'}
        ), name='swagger-ui'),
]