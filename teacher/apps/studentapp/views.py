from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics,status
from apps.studentapp.serializers import StudentSerializer,ActiveOrInactiveSerializer,DeleteSerializer
from apps.student.models import User
from apps.studentapp.models import Student
from apps.studentapp.schemas import ListingSchemas
from django.contrib.auth.hashers import make_password
import random
# Create your views here.
class StudentDetailsCreateOrUpdateApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = {'status_code': 101, 'status': '', 'errors': '', 'message': ''}

    serializer_class=StudentSerializer
    def post(self, request): 
        try:
            student_instance_id=request.data.get('studentid',None) #get student_id from the serializer
            if student_instance_id is not None and student_instance_id:
                student=Student.objects.get(id=student_instance_id) 
                serializer = self.serializer_class(student, data=request.data, context={'request': request})
            else:
                serializer = self.serializer_class(data=request.data, context={'request': request})



            if not serializer.is_valid():
                self.response_format['status_code'] =  status.HTTP_400_BAD_REQUEST,
                self.response_format['status'] =  False,
                self.response_format['errors'] =  serializer.errors,
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            if student_instance_id is None:
                characters="abcdefghijklmnopqrstuvwxyz12222244"
                password  = ''.join(random.choice(characters) for _ in range(8))
                user_obj  = User.objects.get(email=serializer.validated_data['email'])
                if user_obj:
                    user_obj.password=make_password(password)
                    user_obj.save()
                
                
                

            # Create a response dictionary for success cases
            self.response_format['status_code'] =  status.HTTP_201_CREATED,
            self.response_format['status'] =  True,
            self.response_format['data'] =  serializer.data,
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:            
            self.response_format['status_code'] =  status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.response_format['status'] =  False,
            self.response_format['errors'] =  str(e),
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetAllStudentDetails(generics.ListAPIView):
    response_format = {'status_code': 101, 'status': '', 'errors': '', 'message': ''}
    serializer_class = ListingSchemas
    queryset=Student.objects.all()
    
    def get(self, request, *args, **kwargs):
        student_instance_id=request.GET.get('studentid',None) 

        if student_instance_id is not None and student_instance_id:
           student=Student.objects.get(id=student_instance_id)
           serializer = self.serializer_class(student) 

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
        

class ActiveOrInactiveView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = {'status_code': 101, 'status': '', 'errors': '', 'message': ''}
    
    
    serializer_class=ActiveOrInactiveSerializer
    def put(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]      = False
                self.response_format["errors"]      = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            user_instance_id = serializer.validated_data.get('userid')
            serializer  = self.serializer_class(user_instance_id, data=request.data, context={'request': request})

            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]      = False
                self.response_format["errors"]      = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"]     = "success"
            self.response_format["status"]      = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']      = False
            self.response_format['message']     = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentDetailsDelete(generics.DestroyAPIView):
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

            # Get the student instance based on the provided primary key
            student_pk = serializer.validated_data.get('studentid')
            student_pk.user.address.delete()
            student_pk.user.delete()
            student_pk.delete()
            response_data = {
                'status_code': status.HTTP_204_NO_CONTENT,
                'status': True,
                'message': 'Student details deleted successfully'
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
    

