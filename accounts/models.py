from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext as _

class CustomUser(AbstractUser):

    email = models.EmailField(_('email address'), unique=True)
    user_code = models.CharField(max_length=25,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    objects = CustomUserManager()
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions '
                  'granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    def __str__(self):
        return self.email
    


