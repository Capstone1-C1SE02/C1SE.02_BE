from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.http import JsonResponse
from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes


from .models  import *
from .serializers import *

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Xác thực thông tin đăng nhập
        user = authenticate(username=username, password=password)

        if user is not None:
            # Tạo token nếu xác thực thành công
            refresh = RefreshToken.for_user(user)
            message = "Succesfully"
            tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response({"token:":tokens ,"message":message}, status=status.HTTP_200_OK)
        else:
            # Trả về lỗi nếu xác thực thất bại
            return Response({"error": "Incorrect username or password."}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)