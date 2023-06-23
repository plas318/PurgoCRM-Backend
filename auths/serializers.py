from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import User, Department

class CustomSerializer(serializers.ModelSerializer):
    '''
    Custom Serializer add these functionalities:
    Enable Kwarg(Fields) : Enables to select fields when nesting serializers
    e.g.) HospitalSerializer(source='hospital', fields=('hospital_name', 'manager_info'),

    '''
    #Enables kwarg: fields
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        if fields is not None:
            select = set(fields)
            current = set(self.fields.keys())
            for field in current - select:
                self.fields.pop(field)
        super().__init__(*args, **kwargs)

class DepartmentSerializer(CustomSerializer):
    '''
    Department Serializer (General)
    '''
    class Meta:
        model = Department
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'required': True},
        }

class UserSerializer(CustomSerializer):
    '''
    User Serializer (General) password is (write_only)
    '''
    password = serializers.CharField(write_only=True) 

    is_active = serializers.BooleanField(read_only=True)
    
    is_admin = serializers.BooleanField(read_only=True)
    
    dept_name = DepartmentSerializer(source="dept",read_only=True)
    

    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'dept', 'is_admin', 'dept_name', 'is_active']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        else:
            raise serializers.ValidationError('Password is Empty', code='InvalidPassword')
        return super().update(instance, validated_data)

class LoginSerializer(serializers.Serializer):
    '''
    Login Serializer
    
    Takes a given Email, and Password to validate a user

    returns the user on success, or raises a ValidationError
    '''
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username = email,
                password = password)

            if not user:
                raise serializers.ValidationError('Invalid Credentials', code='authorization')
        else:
            raise serializers.ValidationError('Invalid Credentials', code='authorization')
        
        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    '''
    회원가입 Serializer

    Check 항목:
    
    Email이 unique,
    
    password is valid *validate_passowrd 참조

    '''
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset = User.objects.all())]
    )

    name = serializers.CharField(required = True)

    password = serializers.CharField(
        write_only=True,
        required = True,
        validators = [validate_password]
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'name')

    def create(self, validated_data):
        
        user = User.objects.create_user(
            email=validated_data['email'], 
            password=validated_data['password'], 
            name=validated_data['name']
        )
        user.save()
        return user