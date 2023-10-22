from rest_framework  import serializers
from apps.teacherapp.models import Teacher,Qualification
from apps.student.models import Address,User

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
class QualificationSchemas(serializers.ModelSerializer):
    class Meta:
        model=Qualification
        fields=['id','highest_qualification','institution','field_of_study','passoutyear']


class ListingSchemas(serializers.ModelSerializer):
    qualification=serializers.SerializerMethodField("get_qualification")
    user=UserSchemas()
    class Meta:
        model=Teacher
        fields=['id','user','experience_in_years','qualification']

    def get_qualification(self,data):
        serializer=QualificationSchemas(data.qualification)
        return serializer.data