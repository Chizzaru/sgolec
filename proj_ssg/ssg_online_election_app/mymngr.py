from __future__ import unicode_literals
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _ 

class Mymngr(BaseUserManager):
    def create_user(self,student_id,last_name,first_name,address,gender,date_of_birth,password=None,**extra_fields):
        if not student_id:  
            raise ValueError(_('The Student ID must be set'))  
          
        user = self.model(student_id = student_id,last_name=last_name,first_name = first_name,address=address,gender=gender,date_of_birth=date_of_birth, **extra_fields)  
        user.set_password(password)  
        user.save()  
        return user  

    def create_superuser(self,student_id,last_name,first_name,address,gender,date_of_birth,password=None,**extra_fields):
        extra_fields.setdefault('is_staff', True)  
        extra_fields.setdefault('is_superuser', True)  
        extra_fields.setdefault('is_active', True)  

        if extra_fields.get('is_staff') is not True:  
            raise ValueError(_('Superuser must have is_staff=True.'))  
        if extra_fields.get('is_superuser') is not True:  
            raise ValueError(_('Superuser must have is_superuser=True.'))  
            
        return self.create_user(student_id,last_name,first_name,address,gender,date_of_birth, password, **extra_fields)  

    def get_full_name(self):  
        '''  
        Returns the first_name plus the last_name, with a space in between.  
        '''  
        full_name = '%s %s' % (self.first_name, self.last_name)  
        return full_name.strip()  
  
    def get_short_name(self):  
        '''  
        Returns the short name for the user.  
        '''  
        return self.first_name 
