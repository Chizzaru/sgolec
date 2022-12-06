from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .mymngr import Mymngr
from django.utils import timezone  
from django.contrib.auth.models import PermissionsMixin


# User Class Model
class User(AbstractBaseUser, PermissionsMixin):
    objects = Mymngr()

    student_id = models.CharField(max_length=30, unique=True)
    last_name = models.CharField(max_length=80)
    first_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80)
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    date_joined = models.DateTimeField(default=timezone.now)  
    is_superuser = models.BooleanField(default=False)  
    is_staff = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True)  

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS= ['last_name', 'first_name','address','gender','date_of_birth']

    def __str__(self):
        return self.student_id + '-' + self.first_name + ' ' + self.middle_name + ' ' + self.last_name



#Category Class Model
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    number_of_winner = models.IntegerField(default=1)
    checkboxclass = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


#Candidate Class Model
class Candidate(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    candidate_name = models.CharField(max_length=150,unique=True)
    address = models.CharField(max_length=200)
    year_and_section = models.CharField(max_length=50)
    brief_self_intro = models.TextField(max_length=250)
    img_path = models.CharField(max_length=250)

    def __str__(self):
        return self.candidate_name



#VoteVoucher Class Model
class VoteVoucher(models.Model):
    voucher_code = models.CharField(max_length=5, unique=True)
    isUsed = models.BooleanField(default=False)

    def __str__(self):
        return self.voucher_code


#Vote Class Model
class Vote(models.Model):
    vote_voucher = models.ForeignKey(VoteVoucher,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    date_voted = models.DateTimeField(auto_now_add=True, blank=True)


