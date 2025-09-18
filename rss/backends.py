# rss/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    이메일 주소로 로그인할 수 있게 해주는 인증 백엔드
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 이메일로 사용자 찾기
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None