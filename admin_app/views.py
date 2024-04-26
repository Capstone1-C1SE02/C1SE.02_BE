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
from rest_framework.pagination import PageNumberPagination
from .serializers import *

# Create your views here.




####### academic program api #######
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class academic_programList(APIView):
    def get(self, request):
        academic_program1 = academic_program.objects.all()
        serializer = academic_programSerializer(academic_program1, many=True)
        return Response(serializer.data)

    def post(self):
        serializer = academic_programSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class academic_programDetail(APIView):
    def get_object(self, pk):
        try:
            return academic_program.objects.get(pk=pk)
        except academic_program.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        academic_program1 = self.get_object(pk)
        serializer = academic_programSerializer(academic_program1)
        return Response(serializer.data)

    def put(self, request, pk):
        academic_program1 = self.get_object(pk)
        serializer = academic_programSerializer(academic_program1, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        academic_program1 = self.get_object(pk)
        academic_program1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


####### degree api #######
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class degreeList(APIView):
    def get(self, request):
        degree1 = degree.objects.all()
        serializer = degreeSerializer(degree1, many=True)
        return Response(serializer.data)

    def post(self):
        serializer = degreeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class degreeDetail(APIView):
    def get_object(self, pk):
        try:
            return degree.objects.get(pk=pk)
        except degree.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        degree1 = self.get_object(pk)
        serializer = degreeSerializer(degree1)
        return Response(serializer.data)

    def put(self, request, pk):
        degree1 = self.get_object(pk)
        serializer = degreeSerializer(degree1, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        degree1 = self.get_object(pk)
        degree1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)