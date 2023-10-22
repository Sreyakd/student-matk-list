from django.db import models
from apps.student.models import User

# Create your models here.
class Qualification(models.Model):
    QUALIFICATION_TYPE = [
        ('1', 'Diploma'),
        ('2', 'UG'),
        ('3', 'PG'),
    ] 
    highest_qualification = models.CharField(max_length=20, choices=QUALIFICATION_TYPE, null=True, blank=True)
    institution = models.CharField(max_length=100,null=True, blank=True)
    
    field_of_study = models.CharField(max_length=100,null=True, blank=True)
    passoutyear = models.DateField(null=True, blank=True)


class Teacher(models.Model):
    experience_in_years=models.IntegerField(null=True,blank=True)
    qualification = models.ForeignKey(Qualification,on_delete=models.CASCADE,null=True, blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True,blank=True)

    # def __str__(self):
    #     return self.qualification
