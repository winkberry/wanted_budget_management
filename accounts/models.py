from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 그룹과 사용자 권한에 대해 related_name을 변경하여 충돌을 방지
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # related_name 설정
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # related_name 설정
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )