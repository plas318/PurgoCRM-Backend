from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserCreationForm(UserCreationForm):
    '''
    Django Admin에 사용되는 CreationForm
    '''
    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(UserChangeForm):
    '''
    Django Admin에 사용되는 ChangeForm
    '''
    class Meta:
        model = User
        fields = ("email",)