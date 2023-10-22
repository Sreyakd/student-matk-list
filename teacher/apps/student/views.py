# import traceback
from django.shortcuts import render
from rest_framework import generics, status
from django.http import HttpResponse


from .serializer import UserSerializer,DeleteSerializer
from rest_framework.renderers import JSONRenderer
from .models import User , Address
from apps.teacherapp.models import Qualification
from rest_framework.response import Response
from apps.student.schemas import ListingSchemas


class StudentDetailsCreateOrUpdateApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = {'status_code': 101, 'status': '', 'errors': '', 'message': ''}
     
    # queryset = User.objects.all()
    serializer_class = UserSerializer  # Correct the typo in 'StudntSerializer'

    def post(self, request): 
        try:
            student_instance_id=request.data.get('student_id',None) #get student_id from the serializer
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", student_instance_id)

            if student_instance_id is not None and student_instance_id:
                student=User.objects.get(id=student_instance_id) 
                print("student",student.roll_number                                                                                                                                     )
                serializer = self.serializer_class(student, data=request.data, context={'request': request})
  
            else:
                serializer = self.serializer_class(data=request.data, context={'request': request})



            if not serializer.is_valid():
                print("serializerserializer",serializer.errors)
                # Create a response dictionary for error cases
                self.response_format['status_code'] =  status.HTTP_400_BAD_REQUEST,
                self.response_format['status'] =  False,
                self.response_format['errors'] =  serializer.errors,
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            # Create a response dictionary for success cases
            self.response_format['status_code'] =  status.HTTP_201_CREATED,
            self.response_format['status'] =  True,
            self.response_format['data'] =  serializer.data,
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            # import sys, os
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(">>>>>>>>>>>>>>>>>>>>>>>>sd",fname)
            # traceback.print_exc()
            self.response_format['status_code'] =  status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.response_format['status'] =  False,
            self.response_format['errors'] =  str(e),
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        




class GetAllUsertDetails(generics.ListAPIView):
    response_format = {'status_code': 101, 'status': '', 'errors': '', 'message': ''}
    serializer_class = ListingSchemas
    queryset=User.objects.all()
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer=self.serializer_class(queryset, many=True)
        self.response_format['status_code'] = status.HTTP_201_CREATED
        self.response_format["message"]     = "success"
        self.response_format["status"]      = True
        self.response_format["data"]      = serializer.data
        return Response(self.response_format, status=status.HTTP_200_OK)
    
class UserDetailsDelete(generics.DestroyAPIView):
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
            student_pk = serializer.validated_data.get('student_id')
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



   

# Create your views here.
        