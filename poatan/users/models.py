from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('contributor', 'Contributor'),
        ('treasurer', 'Treasurer'),
        ('Chairman', 'Chairman'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='contributor')
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set',  
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set', 
        related_query_name='user',
    )


    def __str__(self):
        return f"{self.username} ({self.role})"