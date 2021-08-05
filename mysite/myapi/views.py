from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer,UserLoginSerializer,UpdateUserSerializer
from .models import User
from django.db.models import Q
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
import jwt,datetime,re
str_jwt_key = 'secret'

# USER REGISTRATION 
# http://localhost:8000/api/register

class RegisterView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def post(self,request):
        str_email = request.data['email']
        str_password = request.data['password']
        str_username = request.data['name']
        user= User.objects.filter(Q(email=str_email) | Q(name=str_username)).first()
        if user :
            raise AuthenticationFailed("Email or UserName already exisits. Please try login.")
        if not str_email:
            raise AuthenticationFailed("Email address can't be empty.")
        elif not str_password:
            raise AuthenticationFailed("Password can't be empty.")
        elif not str_username:
            raise AuthenticationFailed("UserName can't be empty.")
            
        return self.create(request)

# USER LIST
# http://localhost:8000/api/listUser

class ListUserView(generics.GenericAPIView,mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()


    def get(self,request):
        ins_user = User.objects.values_list('id', 'name','email')
        response = Response()
        response.data=set(ins_user)
        return response

# USER LOGIN
# http://localhost:8000/api/login
class LoginView(generics.GenericAPIView,mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()


    def post(self,request):
        
        ins_user = check_login_credentials(request) #checking login credentials
        
        payload ={

                'id':'user.id',
                'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
                'iat':datetime.datetime.utcnow(),
                'first_name':'first_name'

        }	

        token = jwt.encode(payload,str_jwt_key, algorithm='HS256')

        response= Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data ={
                'jwt':token
                }

        return response
        return self.create(request)

# LOG OUT USER
# http://localhost:8000/api/logout

class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={'message':' Logged out successfully'}

        return response


# UPDATE USER INFORMATIONS
# http://localhost:8000/api/update_user

class UpdateUserView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):

    serializer_class=UpdateUserSerializer
    queryset = User.objects.all()

    def post(self,request):
        str_token = request.COOKIES.get('jwt')

        if not str_token:
            raise AuthenticationFailed("User authenication failed, Please login to access the API")
        try:
            dct_payload = jwt.decode(str_token,str_jwt_key,algorithms=['HS256'])
            if not dct_payload or not 'first_name' in dct_payload:
                raise AuthenticationFailed('Payload error.')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Session expired, Please login')
        else:
            ins_user = check_login_credentials(request)
            ins_user.phone = request.data['phone']
            ins_user.city = request.data['city']
            ins_user.address = request.data['address']
            ins_user.save()
            response = Response()
            response.data= {'message':'Updated successfully',
                    'Username':ins_user.name,
                    'UserEmail':ins_user.email,
                    'Phone':ins_user.phone,
                    'City':ins_user.city,
                    'Address':ins_user.address,
                    }
            return response

def check_login_credentials(request):
    """common function to check the login credentials"""
    str_user_name_or_email = request.data['email']
    str_password = request.data['password']
    if re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b', str_user_name_or_email) != None:
        user= User.objects.filter(email=str_user_name_or_email).first()
    else:
        user= User.objects.filter(name=str_user_name_or_email).first()

    if user is None:
        raise AuthenticationFailed("User Not Found")

    if not user.check_password(str_password):
        raise AuthenticationFailed("You have entered incorrect password")
    return user

