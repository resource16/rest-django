from django.db import models

# Create your models here.

class UserGroup(models.Model):
    title = models.CharField(max_length=32)
    
class Role(models.Model):
    title = models.CharField(max_length=32)
    
class UserInfo(models.Model):
    user_type_choices = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP')
    )

    user_type = models.IntegerField(choices=user_type_choices)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, default='')
    role = models.ManyToManyField(Role)
    
    username = models.CharField(max_length=32, unique= True)
    password = models.CharField(max_length=64)

class UserToken(models.Model):
    User = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

