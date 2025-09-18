# rss/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'rss'

urlpatterns = [
    # 메인페이지
    path('', views.PostListView.as_view(), name='home'),
    
    # 인증 관련
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # 게시물 관련
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]