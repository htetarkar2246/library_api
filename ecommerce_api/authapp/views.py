from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import CustomUser, OTP
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  
from .utils import generate_otp, send_otp_email
from django.utils.timezone import now
class RegisterView(APIView):
  def post(sef, request):
    serializer  = UserSerializer(data = request.data)
    if serializer.is_valid():
      user = serializer.save()
      
      # Generate access and refresh tokens
      refresh = RefreshToken.for_user(user)
      access_token = str(refresh.access_token)
            
      response = {
        "meta":{
          "created_at": serializer.data["created_at"],
          "timestamp": str(now()),
        },
        "data": {
          "name": serializer.data["name"],
          "age": serializer.data["age"],
          "email": serializer.data["email"],
          "ph_num": serializer.data["ph_num"],
          "access": access_token,
          "refresh": str(refresh),
        },
      }
      return Response(response, status=status.HTTP_201_CREATED)
    else:
      response = {
          "meta":{
            "timestamp": str(now()),
          },
          "errors": serializer.errors,
          "links": {
            "swagger": "http://127.0.0.1:8000/swagger",
            "redoc": "http://127.0.0.1:8000/redoc",
          }
        }
      return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
  def post(self, request):
    email = request.data.get("email")
    password = request.data.get("password")
        
    if not email or not password:
      response = {
          "meta":{
            "timestamp": str(now()),
          },
          "errors":{
            "email": "Email is required.",
            "password": "Password is required."
          },
          "links": {
            "swagger": "http://127.0.0.1:8000/swagger",
            "redoc": "http://127.0.0.1:8000/redoc",
            "login":"http://127.0.0.1:8000/api/login",
            "forget_password":"http://127.0.0.1:8000/api/forget_password",
            
          }
        }
      return Response(response,status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.filter(email = email).first()
        
    if not user:
      response = {
          "meta":{
            "timestamp": str(now()),
          },
          "errors": "User not found!",
          "links": {
            "swagger": "http://127.0.0.1:8000/swagger",
            "redoc": "http://127.0.0.1:8000/redoc",
            "login":"http://127.0.0.1:8000/api/login",
            "forget_password":"http://127.0.0.1:8000/api/forget_password",
          }
        }
      return Response(response,status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(password):
      response = {
          "meta":{
            "timestamp": str(now()),
          },
          "errors": "Incorrect Password!",
          "links": {
            "swagger": "http://127.0.0.1:8000/swagger",
            "redoc": "http://127.0.0.1:8000/redoc",
            "login":"http://127.0.0.1:8000/api/login",
            "forget_password":"http://127.0.0.1:8000/api/forget_password",
          }
        }
      return Response(response,status=status.HTTP_401_UNAUTHORIZED)
       
      
    # Generate access and refresh tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    response = {
      "meta":{
        "timestamp": str(now()),
      },
      "data":{
        "access": access_token,
        "refresh": str(refresh),
      }
    }
    
    return Response(response, status=status.HTTP_200_OK)
  
class ForgetPasswordView(APIView):
  def post(self, request):
    email = request.data.get("email")
    user = CustomUser.objects.filter(email = email).first()
    
    if not user:
      response = {
          "meta":{
            "timestamp": str(now()),
          },
          "errors": "User not found!",
          "links": {
            "swagger": "http://127.0.0.1:8000/swagger",
            "redoc": "http://127.0.0.1:8000/redoc",
            "login":"http://127.0.0.1:8000/api/login",
            "forget_password":"http://127.0.0.1:8000/api/forget_password",
          }
        }
      return Response(response,status=status.HTTP_404_NOT_FOUND)
    
    # generate otp
    otp_code = generate_otp()
     # Delete expired OTPs before create newone
    OTP.objects.filter(user=user).delete()
    # save otp
    otp = OTP.objects.create(user = user, otp_code = otp_code)
    
    send_otp_email(email, otp)
    response = {
        "meta":{
          "timestamp": str(now()),
        },
        "data": {
          "message": "OTP is successfully sent. OTP is valid for 5 minutes.",
        },
        "links": {
          "swagger": "http://127.0.0.1:8000/swagger",
          "redoc": "http://127.0.0.1:8000/redoc",
          "login":"http://127.0.0.1:8000/api/login",
          "validate_otp":"http://127.0.0.1:8000/api/validate_otp",
          "reset_password":"http://127.0.0.1:8000/api/reset_password"
        }
      }
    return Response(response,status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
  def post(self, request):
    email = request.data.get("email")
    otp_code = request.data.get("otp_code")
    new_password = request.data.get("new_password")
    
    if not email or not otp_code or not new_password:
      response = {
        "meta": {
          "timestamp": str(now()),
        },
        "errors": {
          "email": "Email is required." if not email else None,
          "otp_code": "OTP is required." if not otp_code else None,
          "new_password": "New password is required." if not new_password else None,
        },
        "links": {
          "swagger": "http://127.0.0.1:8000/swagger",
          "redoc": "http://127.0.0.1:8000/redoc",
          "login": "http://127.0.0.1:8000/api/login",
          "forget_password": "http://127.0.0.1:8000/api/forget_password",
          "reset_password": "http://127.0.0.1:8000/api/reset_password",
        },
      }
      return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    user = CustomUser.objects.filter(email = email).first()
    
    if not user:
      response = {
          "meta":{
            "timestamp": str(now()),
          },
          "errors": "User not found!",
          "links": {
            "swagger": "http://127.0.0.1:8000/swagger",
            "redoc": "http://127.0.0.1:8000/redoc",
            "login":"http://127.0.0.1:8000/api/login",
            "forget_password":"http://127.0.0.1:8000/api/forget_password",
            "reset_password":"http://127.0.0.1:8000/api/reset_password"
          }
        }
      return Response(response,status=status.HTTP_404_NOT_FOUND)
   
    otp = OTP.objects.filter(user=user, otp_code=otp_code).first()
    if not otp or not otp.is_valid():
      response = {
        "meta":{
          "timestamp": str(now()),
        },
          "errors": "Invalid OTP!",
          "links": {
          "swagger": "http://127.0.0.1:8000/swagger",
          "redoc": "http://127.0.0.1:8000/redoc",
          "login":"http://127.0.0.1:8000/api/login",
          "forget_password":"http://127.0.0.1:8000/api/forget_password",
          "reset_password":"http://127.0.0.1:8000/api/reset_password"
        }
      }
      return Response(response,status=status.HTTP_404_NOT_FOUND)
    
    # Update the user's password with new password
    user.set_password(new_password)
    user.save()
    
    #delete otp after using
    otp.delete()
    response = {
            "meta": {
                "timestamp": str(now()),
            },
            "data": {
                "message": "Password has been successfully updated.",
            },
            "links": {
                "swagger": "http://127.0.0.1:8000/swagger",
                "redoc": "http://127.0.0.1:8000/redoc",
                "login": "http://127.0.0.1:8000/api/login",
            },
        }
    return Response(response, status=status.HTTP_200_OK)