from django.db import models 
from django.apps import apps

from auths.models import User


class Major(models.Model):
    '''
    Major 전공학위
    '''
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f'{self.name}'

class School(models.Model):
    '''
    School 졸업대학교
    '''
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'

class Doctor(models.Model):
    '''
    Doctor 담당의/원장
    '''
    name = models.CharField(max_length=30)
    graduate_year = models.DateField(null=True)
    major = models.ForeignKey(
        Major, 
        on_delete=models.SET_NULL,
        null=True
    )
    graduate_school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self) -> str:
        return f'{self.name}'

class Hospital(models.Model): 
    '''
    Hospital (심평원Api 기반 병원모델)
    '''
    hospital_id = models.CharField(max_length=255, primary_key=True)
    hospital_name = models.CharField(max_length=255, null=True)
    class_code = models.CharField(max_length=255, null=True)
    class_code_name = models.IntegerField(null=True)
    phone = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    established_at = models.DateTimeField(null=True)
    sggu_name = models.CharField(max_length=255, null=True)
    emdong_name = models.CharField(max_length=255, null=True)
    post_no = models.IntegerField(null=True)
    address = models.CharField(max_length=255, null=True)
    sido_name = models.CharField(max_length=255, null=True)
    sggu_no = models.IntegerField(null=True)
    sido_no = models.IntegerField(null=True)
    general_doctor_count = models.IntegerField(null=True)
    intern_count = models.IntegerField(null=True)
    resident_count = models.IntegerField(null=True)
    fellow_doctor_count = models.IntegerField(null=True)
    # manager = fk user
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    director = models.ForeignKey(
        Doctor, 
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name_plural = 'Hospitals'

    def __str__(self):
        return f'{self.hospital_name} : pk({self.hospital_id}) '

class SalesHistory(models.Model):
    '''
    Sales History Content (Record)
    '''

    STATUS = [
        ('A', "ACT"),
        ('B', "BEST_CASE"),
        ('P', "PIPELINE"),
        ('O', "OPP"),
        ('F', "FUNNEL")
    ]

    hospital = models.ForeignKey(
        Hospital,
        related_name='hosp',
        on_delete=models.CASCADE,
    )
    content = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default='A')
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.hospital} : pk({self.id})'

    class Meta:
        verbose_name = 'History'

class Product(models.Model):
    '''
    Product Model (제품)
    '''
    name = models.CharField(max_length=255, unique=True)
    is_own_product = models.BooleanField(default=False)
    hospital = models.ManyToManyField(Hospital, related_name='product')



