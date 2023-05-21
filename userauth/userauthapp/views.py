import json
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserLoginSerializer,UserRegistrationSerializer,UserRegistrationSerializer



class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
         serializer = UserLoginSerializer(data = request.data)
         if serializer.is_valid(raise_exception=True):
             email=serializer.data.get('email')
             password =serializer.data.get('password')
             print(email+" "+password)
             user = authenticate(email=email, password=password)
             print (user)
             if user is not None:
                    return Response({'msg':'Successful Login'},
                                    status=status.HTTP_200_OK)
             else:
                  return Response({'errors':{'non_field_errors':['Email or password is not valid']}},
                                  status=status.HTTP_404_NOT_FOUND)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg':'Registration Successful'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SelectUserView(APIView):
     def get(self,request,format=None):
        serializer=UserRegistrationSerializer()
        users = User.objects.all()
        # Convert users to JSON format
        user_list = [{'username': user.name, 'mobile': user.mobile, 'address': user.address,  'email': user.email} for user in users]
        # Return the users in JSON format
        return JsonResponse({'users': user_list})
        #return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)