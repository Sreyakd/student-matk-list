from rest_framework import serializers
from apps.student.models import User

class LoginSerilazer(serializers.ModelSerializer):
    email=serializers.EmailField(required=False)
    password=serializers.CharField(required=False)
    class Meta:
        model=User
        fields=['email','password']
    
