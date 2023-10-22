from rest_framework import serializers
from apps.studentapp.models import Student,MarkList
from apps.student.models import User,Address

class AddressSchemas(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields=['id', 'house_name','street_address','city','state','postal_code','country','phone_number']

class UserSchemas(serializers.ModelSerializer):
    address=serializers.SerializerMethodField("get_address")

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'profile_pic','address']

    def get_address(self,data):
        serializer=AddressSchemas(data.address)
        return serializer.data

class ListingSchemas(serializers.ModelSerializer):
    user=UserSchemas()
    class Meta:
        model=Student
        fields=['id','user','father_name','mother_name','roll_number','addmission_date','division','caste','blood_group']
    
    

class MarkListSchemas(serializers.ModelSerializer):
    class Meta:
        model=MarkList
        fields=['id','student_id','subject_name','exam_date','exam_name','mark_obtained']

        

        
