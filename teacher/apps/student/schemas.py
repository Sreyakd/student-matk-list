from rest_framework import serializers
from apps.student.models import User, Address
from apps.teacherapp.models import Qualification

class QualificationSchemas(serializers.ModelSerializer):
    class Meta:
        model=Qualification
        fields=['id','highest_qualification','institution','field_of_study','passoutyear']

class AddressSchemas(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields=['id', 'house_name','street_address','city','state','postal_code','country','phone_number']

class ListingSchemas(serializers.ModelSerializer):
    
    qualification=serializers.SerializerMethodField("get_qualification")
    address=serializers.SerializerMethodField("get_address")
    
    class Meta:
        model=User
        fields=['id', 'user_type','roll_number','first_name','last_name','qualification', 'email','date_of_birth','gender','address','admission_date','current_class',]
    
    
    def get_qualification(self,data):

        serializer=QualificationSchemas(data.qualification)
        return serializer.data
    

    def get_address(self,data):
        serializer=AddressSchemas(data.address)
        return serializer.data
    
    
