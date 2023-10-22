from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics,status
from apps.teacherapp.serializer import TeacherSerializer,DeleteSerializer
from apps.teacherapp.models import Teacher
from apps.teacherapp.schemas import ListingSchemas
from django.contrib.auth.hashers import make_password
from apps.student.models import User

import random

# Create your views here.
class TeacherDetailsCreateOrUpdateApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = {'status_code': 101, 'status': '', 'errors': '', 'message': ''}

    serializer_class=TeacherSerializer
    def post(self, request): 
        try:
            teacher_instance_id=request.data.get('teacherid',None) #get teacher_id from the serializer
            if teacher_instance_id is not None and teacher_instance_id:
                teacher=Teacher.objects.get(id=teacher_instance_id) 
                serializer = self.serializer_class(teacher, data=request.data, context={'request': request})
            else:
                serializer = self.serializer_class(data=request.data, context={'request': request})



            if not serializer.is_valid():
                print("serializerserializer",serializer.errors)
                self.response_format['status_code'] =  status.HTTP_400_BAD_REQUEST,
                self.response_format['status'] =  False,
                self.response_format['errors'] =  serializer.errors,
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            if teacher_instance_id is None:
                characters="abcdefghijklmnopqrstuvwxyz12222244"
                # password  = ''.join(random.choice(characters) for _ in range(8))
                password  = '12345678'
                print(">>>>>>>>>",password)
                user_obj  = User.objects.get(email=serializer.validated_data.get('email', ''))
                if user_obj:
                    # user_obj.password=make_password(password)                   
                    user_obj.set_password(password)
                    user_obj.save()



            self.response_format['status_code'] =  status.HTTP_201_CREATED,
            self.response_format['status'] =  True,
            self.response_format['data'] =  serializer.data,
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:            
            self.response_format['status_code'] =  status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.response_format['status'] =  False,
            self.response_format['errors'] =  str(e),
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAllTeacherDetails(generics.ListAPIView):
    response_format = {'status_code': 101, 'status': '', 'errors': '', 'message': ''}
    serializer_class = ListingSchemas
    queryset=Teacher.objects.all()
    
    def get(self, request, *args, **kwargs):
        teacher_instance_id=request.GET.get('teacherid',None) 

        if teacher_instance_id is not None and teacher_instance_id:
           teacher=Teacher.objects.get(id=teacher_instance_id)
           serializer = self.serializer_class(teacher) 

           self.response_format['status_code'] = status.HTTP_200_OK
           self.response_format["message"] = "success"
           self.response_format["status"] = True
           self.response_format["data"] = serializer.data
           return Response(self.response_format, status=status.HTTP_200_OK)


        else:
           queryset = self.get_queryset()
           serializer=self.serializer_class(queryset, many=True)
           self.response_format['status_code'] = status.HTTP_200_OK
           self.response_format["message"]     = "success"
           self.response_format["status"]      = True
           self.response_format["data"]      = serializer.data
           return Response(self.response_format, status=status.HTTP_200_OK)
        

class TeacherDetailsDelete(generics.DestroyAPIView):
    serializer_class = DeleteSerializer
    def destroy(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                response_data = {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'status': False,
                    'errors': serializer.errors,
                    'message': 'Validation Error'
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Get the teacher instance based on the provided primary key
            teacher_pk = serializer.validated_data.get('teacherid')
            teacher_pk.qualification.delete()
            teacher_pk.user.address.delete()
            teacher_pk.user.delete()
            teacher_pk.delete()
            response_data = {
                'status_code': status.HTTP_204_NO_CONTENT,
                'status': True,
                'message': 'Teacher details deleted successfully'
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            response_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': False,
                'errors': str(e),
                'message': 'Internal Server Error'
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



