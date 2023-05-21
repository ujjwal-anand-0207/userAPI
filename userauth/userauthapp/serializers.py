
from django.db.models import fields
from rest_framework import serializers
from .models import User
 
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('cust_id','cust_mobile','cust_username','cust_password','cust_name')

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']

class UserSelectSerializer():
    class Meta:
        model=User
        
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    # For confirming password field during registration process
    password2 =serializers.CharField(style ={'input_type':'password'},
                                         write_only=True)
    class Meta:
        model = User
        
        fields =['email','name', "mobile",'address','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    #validating Password and confirm password
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password doesn't match")
        return attrs
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)