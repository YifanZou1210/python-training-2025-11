from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser): # django中可以自定义user
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True)
    # django里AbstractBaseUser/AbstractUser定义的特殊class attribute, 用来告诉django 哪个字段作为登陆凭证primary identifier
    USERNAME_FIELD='email'# class attribute, 不是metadata, 认证auth时用email字段代替username, default是username
    REQUIRED_FIELDS=['username'] # 用于createsuperuser时要求必须提供的字段（除了username_field的动态字段以外）
    # 其他attribute
    # is_anonymous = False 标识用户是否匿名，不可手动改
    # is_authenticated = True, 用户是否通过auth
    # email_field  = 'email' 默认email字段名， 一般不需要
    
    
    def __str__(self) -> str:
        return self.email

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    published = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.title