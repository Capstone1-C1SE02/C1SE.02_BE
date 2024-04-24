from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
class LogoutSerializer(serializers.Serializer):
    pass

class AcademicIntakeSessionSerializer(serializers.Serializer):
    class Meta:
        model = academic_intake_session
        fields = '__all__'
