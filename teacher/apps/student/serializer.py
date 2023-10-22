from rest_framework import serializers
from .models import User,Address
from apps.teacherapp.models import Qualification
# from rest_framework import status
# from rest_framework.response import Response

class QualificationSerializer(serializers.ModelSerializer):
    qualification_instance=serializers.PrimaryKeyRelatedField(queryset=Qualification.objects.all(),required=False)
    highest_qualification = serializers.CharField()
    institution = serializers.CharField()
    
    field_of_study = serializers.CharField()
    passoutyear = serializers.DateField()
    
    class Meta:
        model=Qualification
        fields=['qualification_instance','highest_qualification','institution','field_of_study','passoutyear']

class AddressSerializer(serializers.ModelSerializer):
    address_instance=serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(),required=False)

    house_name=serializers.CharField()                                                                                                                                                                                                                                                                                                                                             
    street_address = serializers.CharField()
    city = serializers.CharField()
    state =serializers.CharField()
    postal_code = serializers.CharField()
    country = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model=Address
        fields=['address_instance','house_name','street_address','city','state','postal_code','country','phone_number']

    
    

class UserSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(),required=False, )
    user_type       = serializers.CharField()
    # roll_number     = serializers.CharField(allow_null=True)
    first_name      = serializers.CharField()
    last_name       = serializers.CharField()
    email           = serializers.EmailField()

    qualification   = QualificationSerializer()
    date_of_birth   = serializers.DateField()
    gender          = serializers.CharField()
    address         = AddressSerializer()
    # admission_date  = serializers.DateField(allow_null=True)
    # current_class   = serializers.CharField(allow_null=True)
    # current_class   = serializers.CharField(allow_null=True)
    profile_pic     = serializers.ImageField(required=False)
    is_active       =serializers.BooleanField(required=False)

    

    class Meta:
        model=User
        fields=['student_id','user_type','first_name','last_name','email','date_of_birth','gender','address','profile_pic']

    def create(self, validated_data):
        print(1)
        instance=User()
        
        instance.user_type=validated_data.get('choices')
        # instance.roll_number=validated_data.get('roll_number')
        instance.first_name=validated_data.get('first_name')
        instance.last_name=validated_data.get('last_name')
        instance.email=validated_data.get('email')
        instance.date_of_birth=validated_data.get('date_of_birth')
        instance.gender=validated_data.get('gender')
        # instance.admission_date=validated_data.get('admission_date')
        instance.profile_pic=validated_data.get('profile_pic')

        address_obj=validated_data.get('address')
        address=Address(
            house_name=address_obj['house_name'],
            street_address=address_obj['street_address'],
            city=address_obj['city'],
            state=address_obj['state'],                                                                                                                                                                                                                                                                                                                                                                             
            postal_code=address_obj['postal_code'],
            country=address_obj['country'],
            phone_number=address_obj['phone_number']

        )
        address.save()
        instance.address=address
        instance.save()

        qualification_obj= validated_data.get('qualification')
        qualification = Qualification(
            highest_qualification=qualification_obj['highest_qualification'],
            field_of_study=qualification_obj['field_of_study'],
            institution=qualification_obj['institution'],
            passoutyear=qualification_obj['passoutyear']           
        )
        qualification.save()
        instance.qualification = qualification
        instance.qualification.save()
        return instance
    
    def update(self, instance, validated_data):
            print("validated_data",validated_data)
            print("instance",instance)
        
            instance.user_type = validated_data.get('user_type', instance.user_type)
            instance.email = validated_data.get('email', instance.email)
            instance.roll_number = validated_data.get('roll_number', instance.roll_number)
            instance.first_name = validated_data.get('first_name', instance.first_name)                                                                             
            instance.last_name = validated_data.get('last_name', instance.last_name)                                                                                                                

            # Update qualification details if provided
            qualification_data = validated_data.get('qualification')
            if qualification_data:

                qualification = Qualification.objects.get(id=instance.qualification.id) if instance.qualification else Qualification()
                qualification.highest_qualification = qualification_data.get('highest_qualification', qualification.highest_qualification)
                qualification.field_of_study = qualification_data.get('field_of_study', qualification.field_of_study)
                qualification.institution = qualification_data.get('institution', qualification.institution)
                qualification.passoutyear = qualification_data.get('passoutyear', qualification.passoutyear)
                qualification.save()
                instance.qualification = qualification

            # Update address details if provided
            address_data = validated_data.get('address')

            print("address_data",address_data)
            if address_data:                                                                                                                                    

                address = Address.objects.get(id=instance.address.id)
                address.house_name   = address_data.get('house_name', None)
                address.street_address = address_data.get('street_address', address.street_address)
                address.city = address_data.get('city', address.city)
                address.state = address_data.get('state', address.state)
                address.postal_code = address_data.get('postal_code', address.postal_code)
                address.country = address_data.get('country', address.country)
                address.phone_number = address_data.get('phone_number', address.phone_number)
                address.save()                                                                                                                          
                instance.address = address

            instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
            instance.gender = validated_data.get('gender', instance.gender)
            instance.admission_date = validated_data.get('admission_date', instance.admission_date)
            instance.current_class = validated_data.get('current_class', instance.current_class)
            instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)        
            
        
            instance.save()
            
            return instance
    


    

class DeleteSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(),required=False)
    class Meta:
        model=User
        fields=['student_id']



        






