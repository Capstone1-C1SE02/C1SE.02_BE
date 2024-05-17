from rest_framework import serializers
from admin_app.models import *

class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = degree
        fields = ["DEGREE_NAME"]

class AcademicProgram_Serializer(serializers.ModelSerializer):
    DEGREE = DegreeSerializer(source='DEGREE_ID', many=False)
    class Meta:
        model = academic_program
        fields = ["ACADEMIC_PROGRAM_NAME","DEGREE"]

class StudentSerializer(serializers.ModelSerializer):
    STUDENT_NAME = serializers.SerializerMethodField()
    class Meta:
        model = student
        fields = ["STUDET_NAME"]
    def get_STUDENT_NAME(self, obj):
        return f"{obj.LAST_NAME} {obj.MIDDLE_NAME} {obj.FIRST_NAME}"
    
class DiplomaManagementProfileSerializer(serializers.ModelSerializer):
    ACADEMIC_PROGRAM = AcademicProgram_Serializer(source='ACADEMIC_PROGRAM_ID', many=False)
    STUDENT = StudentSerializer(source='STUDENT_ID_NUMBER',many=False)
    BIRTH_DATE = serializers.DateField(source='STUDENT_ID_NUMBER.BIRTH_DATE')
    class Meta:
        model = diploma_management_profile
        exclude  = ["ACADEMIC_PROGRAM_ID","user","DIPLOMA_MANAGEMENT_PROFILE_ID","COMMENT","DATE_UPDATED","APPORVEDY"]
    
    
class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()