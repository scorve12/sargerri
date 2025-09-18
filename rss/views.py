# rss/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404
from django import forms
from .models import Post, Tag, CustomUser

# 커스텀 회원가입 폼
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='이메일')
    name = forms.CharField(max_length=100, required=True, label='이름')
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, required=True, label='성별')
    age = forms.IntegerField(required=True, label='나이')
    interest_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='관심태그'
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'gender', 'age', 'interest_tags', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.gender = self.cleaned_data['gender']
        user.age = self.cleaned_data['age']
        if commit:
            user.save()
            self.save_m2m()
        return user

# 프로필 수정 폼
class ProfileUpdateForm(forms.ModelForm):
    interest_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='관심태그'
    )
    
    class Meta:
        model = CustomUser
        fields = ['name', 'gender', 'age', 'interest_tags']
        labels = {
            'name': '이름',
            'gender': '성별',
            'age': '나이',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# 회원가입 뷰
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('rss:login')
    template_name = 'registration/signup.html'

# 프로필 보기
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'rss/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['user_posts'] = Post.objects.filter(author=user).order_by('-created_at')[:5]  # 최근 5개 게시물
        context['total_posts'] = Post.objects.filter(author=user).count()
        return context

# 프로필 수정
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'rss/profile_edit.html'
    success_url = reverse_lazy('rss:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, '프로필이 성공적으로 수정되었습니다!')
        return super().form_valid(form)

# 메인페이지 - 게시물 목록
class PostListView(ListView):
    model = Post
    template_name = 'rss/home.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related('tags')

# 게시물 상세보기
class PostDetailView(DetailView):
    model = Post
    template_name = 'rss/post_detail.html'
    context_object_name = 'post'

# 게시물 작성
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'photo', 'tags', 'start_date', 'end_date']
    template_name = 'rss/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '게시물이 성공적으로 작성되었습니다!')
        return super().form_valid(form)

# 게시물 삭제
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('rss:home')
    template_name = 'rss/post_confirm_delete.html'
    context_object_name = 'post'
    
    def get_object(self, queryset=None):
        """작성자만 삭제할 수 있도록 권한 체크"""
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise Http404("삭제 권한이 없습니다.")
        return obj
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '게시물이 성공적으로 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)