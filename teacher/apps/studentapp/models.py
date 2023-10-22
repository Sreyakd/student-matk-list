from django.db import models
from apps.student.models import User                                                                                                                                                                                                                                                                                                                                                            
# Create your models here.

class Student(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    father_name=models.CharField(max_length=100,null=True,blank=True)
    mother_name=models.CharField(max_length=100,null=True,blank=True)
    roll_number = models.CharField(max_length=20, null=True, blank=True,unique=True)
    addmission_date=models.DateField(null=True,blank=True)
    division = models.CharField(max_length=50, null=True, blank=True)
    caste=models.CharField(max_length=100,null=True,blank=True)
    blood_group=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.roll_number
    
class MarkList(models.Model):
    class_teacher = 
    subject_teacher =
    exam_date=models.DateField(null=True,blank=True)
    exam_name=models.CharField(max_length=120,null=True,blank=True)
    marks_obtained=models.PositiveIntegerField(null=True,blank=True)
    subject_name=models.CharField(max_length=120,null=True,blank=True) 
        
    def __str__(self):
        return str(self.pk) 
        


