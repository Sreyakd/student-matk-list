from rest_framework import serializers
from apps.student.models import User

class LoginSchema(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['id','first_name','last_name','email']