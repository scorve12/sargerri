# blog/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# 태그 모델
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='태그명')
    
    class Meta:
        verbose_name = '태그'
        verbose_name_plural = '태그들'
    
    def __str__(self):
        return self.name

# 사용자 모델 (기본 User 확장)
class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
        ('O', '기타'),
    ]
    
    email = models.EmailField(unique=True, verbose_name='이메일')
    name = models.CharField(max_length=100, verbose_name='이름')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='성별')
    age = models.IntegerField(verbose_name='나이')
    interest_tags = models.ManyToManyField(Tag, blank=True, verbose_name='관심태그')
    
    USERNAME_FIELD = 'email'  # 이메일로 로그인
    REQUIRED_FIELDS = ['username', 'name', 'gender', 'age']
    
    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'
    
    def __str__(self):
        return self.name

# 게시물 모델
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    photo = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='사진')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='작성자')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='태그')
    start_date = models.DateField(verbose_name='시작일')
    end_date = models.DateField(verbose_name='종료일')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '게시물'
        verbose_name_plural = '게시물들'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})