from rest_framework import serializers
from apps.studentapp.models import Student,MarkList
from apps.student.models import Address,User


class AddressSerializer(serializers.ModelSerializer):
    address_instance=  serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(),required=False)
    house_name = serializers.CharField()
    street_address = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    postal_code = serializers.CharField()
    country = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model=Address
        fields= ['address_instance','house_name','street_address','city','state','postal_code','country','phone_number']


#serializer for student model
class StudentSerializer(serializers.ModelSerializer):
    studentid=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(),required=False)
    user_type = serializers.CharField(required=False)
    email  = serializers.EmailField(required=False)
    roll_number = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    gender = serializers.CharField(required=False)
    address =AddressSerializer(required=False)
    addmission_date = serializers.DateField(required=False)
    profile_pic=serializers.ImageField(required=False)
    blood_group  = serializers.CharField(required=False)
    caste  = serializers.CharField(required=False)
    father_name  = serializers.CharField(required=False)
    mother_name  = serializers.CharField(required=False)
    division  =serializers.CharField(required=False) 

    class Meta: 
        model=Student
        fields= ['studentid','user_type','email','roll_number','first_name','last_name','date_of_birth','gender','address'
                 ,'addmission_date','profile_pic','blood_group','caste','father_name','mother_name','division']
    
    def validate(self, attrs):
        return super().validate(attrs) 
    
    def create(self,validated_data):
        instance = User.objects.create(
        email=validated_data.get('email', None),
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
        student_instance=Student()
        student_instance.user_id=instance.id
        student_instance.blood_group=validated_data.get('blood_group')
        student_instance.caste=validated_data.get('caste')                                                                                                                                                                                                                              
        student_instance.father_name=validated_data.get('father_name')
        student_instance.mother_name=validated_data.get('mother_name')
        student_instance.addmission_date=validated_data.get('addmission_date', None)
        student_instance.division=validated_data.get('division')
        student_instance.roll_number=validated_data.get('roll_number')


        student_instance.save()                                                                                                                                                                             

        return student_instance                                                                                 

    def update(self, student_instance, validated_data):
        student_instance.user.email = validated_data.get('email', student_instance.user.email)
        student_instance.user.user_type=validated_data.get('user_type',student_instance.user.user_type)
        student_instance.user.first_name = validated_data.get('first_name', student_instance.user.first_name)
        student_instance.user.last_name=validated_data.get('last_name',student_instance.user.last_name)
        student_instance.user.date_of_birth = validated_data.get('date_of_birth', student_instance.user.date_of_birth)
        student_instance.user.gender = validated_data.get('gender', student_instance.user.gender)
        student_instance.user.profile_pic = validated_data.get('profile_pic', student_instance.user.profile_pic)
        address_data = validated_data.get('address')


        if address_data:
            address_id = student_instance.user.address.id
            
            student_instance.user.address = Address.objects.get(id=address_id)
            student_instance.user.address.house_name   = address_data.get('house_name', None)
            student_instance.user.address.street_address = address_data.get('street_address', student_instance.user.address.street_address)
            student_instance.user.address.city = address_data.get('city', student_instance.user.address.city)
            student_instance.user.address.postal_code = address_data.get('postal_code', student_instance.user.address.postal_code)
            student_instance.user.address.country = address_data.get('country', student_instance.user.address.country)
            student_instance.user.address.phone_number = address_data.get('phone_number', student_instance.user.address.phone_number)
            student_instance.user.address.save()
        student_instance.user.save()
            

        student_instance.blood_group = validated_data.get('blood_group', student_instance.blood_group)
        student_instance.caste = validated_data.get('caste', student_instance.caste)
        student_instance.father_name = validated_data.get('father_name', student_instance.father_name)
        student_instance.mother_name = validated_data.get('mother_name', student_instance.mother_name)
        student_instance.division=validated_data.get('division',student_instance.division)
        student_instance.roll_number=validated_data.get('roll_number',student_instance.roll_number)
        student_instance.save()
        return student_instance
    

class ActiveOrInactiveSerializer(serializers.ModelSerializer):
    userid=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=False)
    class Meta:
        model=User
        fields=['userid']

    def validate(self, attrs):
        return super().validate(attrs)
    
    def update(self, student_instance, validated_data):
        student_instance.is_active=True if not student_instance.is_active else False
        student_instance.save()
        return student_instance 
    

class DeleteSerializer(serializers.ModelSerializer):
    studentid = serializers.PrimaryKeyRelatedField(queryset = Student.objects.all(),required=False)
    class Meta:
        model=Student
        fields=['studentid']

class MarkListSerializer(serializers.ModelSerializer):
    markid=serializers.PrimaryKeyRelatedField(queryset=MarkList.objects.all(),required=False)
    exam_date=serializers.DateField(required=False)
    exam_name=serializers.CharField(required=False)
    marks_obtained=serializers.IntegerField(required=False)
    subject_name=serializers.CharField(required=False)
    class Meta:
        model=MarkList
        fields=['markid','exam_date','exam_name','marks_obtained','subject_name']

        


        




        
        



            
        



            


     
                                                                                    




                                                                             

                                                                             


        

        


    
        
    
        





        







    



    

