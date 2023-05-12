from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from rest_framework.permissions import BasePermission

from .models import Blog

import uuid

class CanManageBlog(BasePermission):
    def has_permission(self, request, view):
        permission_name = f"blogs.can_manage_blog{request.data.get('blog')}"
        return request.user.has_perm(permission_name)

class CanManagePosts(BasePermission):
    def has_permission(self, request, view):
        permission_name = f"blogs.can_manage_posts{uuid.UUID(request.data.get('blog'))}"
        return request.user.has_perm(permission_name)

class CanManageMembers(BasePermission):
    def has_permission(self, request, view):
        permission_name = f"blogs.can_manage_members{request.data.get('blog')}"
        return request.user.has_perm(permission_name)


content_type = ContentType.objects.get_for_model(Blog)


def create_blog_permissions_and_groups(id):
    # This should create the admin group and the permissions that I need when I create a blog
    admin_group,created = Group.objects.get_or_create(name=f'admin{id}')

    can_manage_posts,created = Permission.objects.get_or_create(
                        name='Can manage posts',
                        codename=f'can_manage_posts{id}',
                        content_type=content_type
    )

    can_manage_blog,created = Permission.objects.get_or_create(
        name='Can edit blog settings',
        codename=f'can_manage_blog{id}',
        content_type=content_type
    )

    can_manage_members,created = Permission.objects.get_or_create(
        name='Can manage members',
        codename=f'can_manage_members{id}',
        content_type=content_type
    )

    admin_group.permissions.add(
        can_manage_posts,
        can_manage_blog,
        can_manage_members,
    )
