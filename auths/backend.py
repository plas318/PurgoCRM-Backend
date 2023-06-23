from django.contrib.auth.backends import ModelBackend

from .models import User

class UserBackend(ModelBackend):
    '''
    Custom User Backend 

    Django가 기본으로 사용하는 Backend를 Custom User Model을 사용하도록 변경
    
    '''
    def authenticate(self, request, username= None, password=None, **kwargs):
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        
            if user.check_password(password):
                return user