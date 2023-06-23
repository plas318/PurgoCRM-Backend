from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        '''
        Creates a user with credentials
        '''

        if not email:
            raise ValueError('Email is required')

        email =self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        '''
        Creates a superuser(admin) with credentials
        '''
        
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must be admin')

        return self.create_user(email, password, **extra_fields)


class Department(models.Model):
    '''
    Department Model (부서 or 팀)
    '''
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class User(AbstractBaseUser, PermissionsMixin):
    '''
    User Model (영업사원)
    '''

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    dept = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL,
        related_name='employees',
        null=True
    )

    is_active = models.BooleanField(default=True) # 계정 활성화 상태
    is_admin = models.BooleanField(default=False) # 커스텀 Permission
    is_staff = models.BooleanField(default=False) # Django admin permission
    is_superuser = models.BooleanField(default=False) # Django admin & crud for all models
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'name',
    ]

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    

    def __str__(self):
       return f'{self.email} {self.name}'

