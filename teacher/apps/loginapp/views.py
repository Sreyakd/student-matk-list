from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from apps.loginapp.serializer import LoginSerilazer
from apps.loginapp.schemas import LoginSchema
from rest_framework import generics,status
from apps.student.models import User
from django.db.models import Q
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from apps.loginapp.helpers import DataEncryption
import json
from teacher import settings



# Create your views here.
class LoginView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = {'status_code': 101, 'status': '', 'errors': '', 'message': ''}
    
    serializer_class=LoginSerilazer
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]      = False
                self.response_format["errors"]      = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            email    = serializer.validated_data.get('email', '')
            password = serializer.validated_data.get('password', '')
            try:
                user_instance = User.objects.get(email=email)
            except:
                user_instance = None
            
        

            user = auth.authenticate(username=user_instance.email, password=password)
            if user:
                serializer = LoginSchema(user, context={"request": request})
                if not user.is_active:
                    data = {'user': {}, 'token': '', 'refresh': ''}
                    self.response_format['status_code'] = status.HTTP_202_ACCEPTED
                    self.response_format["data"]        = data
                    self.response_format["status"]      = False
                    self.response_format["message"]     = 'account_tem_suspended'
                    return Response(self.response_format, status=status.HTTP_200_OK)
                else:
                    final_out         = json.dumps(serializer.data)
                    key               = settings.STUDENT_MARK
                    encrypted_data    = DataEncryption.encrypt(key, final_out)
                    access_tokens     = AccessToken.for_user(user)
                    refresh_token     = RefreshToken.for_user(user)             
                
                    
                    data = {'user': encrypted_data, 'token': str(access_tokens), 'refresh': str(refresh_token)}
                    self.response_format['status_code'] = status.HTTP_200_OK
                    self.response_format["data"]        = data
                    self.response_format["status"]      = True
                    return Response(self.response_format, status=status.HTTP_200_OK)

            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"]     = 'invalid_credentials'
                self.response_format["status"]      = False
                return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

            
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']      = False
            self.response_format['message']     = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        



        
