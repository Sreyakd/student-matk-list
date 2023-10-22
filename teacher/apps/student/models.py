from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager, PermissionsMixin
    
    
)
from django.contrib.auth.models import User                                                                                                                     
class Address(models.Model):
    house_name=models.CharField(max_length=100,null=True, blank=True)                                                                                                                                                                                                                                                                                                                                             
    street_address = models.CharField(max_length=255,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True, blank=True)
    postal_code = models.CharField(max_length=20,null=True, blank=True)
    country = models.CharField(max_length=100,null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.house_name
        

class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, user_type = 1, is_admin=True, is_verified=True, **extra_fields
        )

    def customers(self):
        return self.get_queryset().filter(
            Q(is_staff=False) | (Q(is_staff=True) & Q(orders__isnull=False))
        )

    def staff(self):
        return self.get_queryset().filter(is_staff=True)
 


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [
        ('1', 'Student'),
        ('2', 'Teacher'),
        
    ]

    GENDER_TYPES=[
        ('1','female'),
        ('2','male'),
        ('3','other')
    ]

    user_type=models.CharField(max_length=20, choices=USER_TYPES, null=True, blank=True)
    # roll_number = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email=models.EmailField(unique=True,null=True,blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True,choices=GENDER_TYPES)
    address = models.ForeignKey(Address,on_delete=models.CASCADE, null=True,blank=True)
    # admission_date = models.DateField(null=True, blank=True)
    # current_class = models.CharField(max_length=50, null=True, blank=True)
    profile_pic=models.ImageField(null=True, blank=True)
    is_active=models.BooleanField(default=True, null=True,blank=True)


    USERNAME_FIELD="email"
    objects = UserManager()


    def __str__(self):
        return str(self.pk)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
        



    













                                                                                                                                                                                                    