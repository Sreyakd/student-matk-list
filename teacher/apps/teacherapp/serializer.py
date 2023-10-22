from rest_framework import serializers
from apps.teacherapp.models import Qualification,Teacher
from apps.studentapp.serializers import AddressSerializer
from apps.student.models import User,Address




class QualificationSerializer(serializers.ModelSerializer):
    qualification_instance=serializers.PrimaryKeyRelatedField(queryset=Qualification.objects.all(),required=False)
    highest_qualification = serializers.CharField()
    institution = serializers.CharField()
    
    field_of_study = serializers.CharField()
    passoutyear = serializers.DateField()
    
    class Meta:
        model=Qualification
        fields=['qualification_instance','highest_qualification','institution','field_of_study','passoutyear']

class TeacherSerializer(serializers.ModelSerializer):
    teacherid=serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(),required=False)
    user_type=serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email  = serializers.EmailField(required=False)
    date_of_birth = serializers.DateField(required=False)
    gender = serializers.CharField(required=False)
    address =AddressSerializer(required=False)
    profile_pic=serializers.ImageField(required=False)
    qualification=QualificationSerializer(required=False)
    experience_in_years=serializers.IntegerField(required=False)


    class Meta:
        model=Teacher
        fields=['teacherid','user_type','first_name','last_name','email','date_of_birth','gender','address','profile_pic','experience_in_years','qualification']


    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self,validated_data):
        instance = User.objects.create(
        email=validated_data.get('email'),
        user_type=validated_data.get('user_type'),
        first_name=validated_data.get('first_name'),
        last_name=validated_data.get('last_name'),
        date_of_birth=validated_data.get('date_of_birth'),
        gender=validated_data.get('gender'),
        profile_pic=validated_data.get('profile_pic')
        )
        address_object = validated_data.get('address')
        if address_object:
            address_row = Address(
                house_name=address_object['house_name'],
                street_address=address_object['street_address'],
                city=address_object['city'],
                state=address_object['state'], 
                postal_code=address_object['postal_code'],
                country=address_object['country'],
                phone_number=address_object['phone_number'],
            )
            address_row.save()
            instance.address = address_row
        instance.save()
        teacher_instance=Teacher()
        teacher_instance.user_id=instance.id
        teacher_instance.experience_in_years=validated_data.get('experience_in_years')
        qualification_obj= validated_data.get('qualification')
        if qualification_obj:
            qualification = Qualification(
            highest_qualification=qualification_obj['highest_qualification'],
            field_of_study=qualification_obj['field_of_study'],
            institution=qualification_obj['institution'],
            passoutyear=qualification_obj['passoutyear']           
            )
        
            qualification.save()
            teacher_instance.qualification = qualification
        teacher_instance.qualification.save()
        teacher_instance.save()
        return teacher_instance
                                   
    def update(self, teacher_instance, validated_data):
        teacher_instance.user.email = validated_data.get('email', teacher_instance.user.email)
        teacher_instance.user.user_type=validated_data.get('user_type',teacher_instance.user.user_type)
        teacher_instance.user.first_name = validated_data.get('first_name', teacher_instance.user.first_name)
        teacher_instance.user.last_name=validated_data.get('last_name',teacher_instance.user.last_name)
        teacher_instance.user.date_of_birth = validated_data.get('date_of_birth', teacher_instance.user.date_of_birth)
        teacher_instance.user.gender = validated_data.get('gender', teacher_instance.user.gender)
        teacher_instance.user.profile_pic = validated_data.get('profile_pic', teacher_instance.user.profile_pic)
        address_data = validated_data.get('address')


        if address_data:
            address_id = teacher_instance.user.address.id
            
            teacher_instance.user.address = Address.objects.get(id=address_id)
            teacher_instance.user.address.house_name   = address_data.get('house_name', None)
            teacher_instance.user.address.street_address = address_data.get('street_address', teacher_instance.user.address.street_address)
            teacher_instance.user.address.city = address_data.get('city', teacher_instance.user.address.city)
            teacher_instance.user.address.postal_code = address_data.get('postal_code', teacher_instance.user.address.postal_code)
            teacher_instance.user.address.country = address_data.get('country', teacher_instance.user.address.country)
            teacher_instance.user.address.phone_number = address_data.get('phone_number', teacher_instance.user.address.phone_number)
            teacher_instance.user.address.save()
        teacher_instance.user.save()
        qualification_data=validated_data.get('qualification')
        if qualification_data:
            qualification_id=teacher_instance.qualification.id
            teacher_instance.qualification=Qualification.objects.get(id=qualification_id)
            teacher_instance.qualification.highest_qualification = qualification_data.get('highest_qualification', teacher_instance.qualification.highest_qualification)
            teacher_instance.qualification.field_of_study = qualification_data.get('field_of_study', teacher_instance.qualification.field_of_study)
            teacher_instance.qualification.institution = qualification_data.get('institution', teacher_instance.qualification.institution)
            teacher_instance.qualification.passoutyear = qualification_data.get('passoutyear', teacher_instance.qualification.passoutyear)
            teacher_instance.qualification.save()
        teacher_instance.experience_in_years=validated_data.get('experience_in_years',teacher_instance.experience_in_years)
        teacher_instance.save()
        return teacher_instance
    
class DeleteSerializer(serializers.ModelSerializer):
    teacherid = serializers.PrimaryKeyRelatedField(queryset = Teacher.objects.all(),required=False)
    class Meta:
        model=Teacher
        fields=['teacherid']