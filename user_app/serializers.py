from rest_framework import serializers
from admin_app.models import *

class AcademicProgram_Serializer(serializers.ModelSerializer):
    class Meta:
        model = academic_program
        fields = ["ACADEMIC_PROGRAM_ID","ACADEMIC_PROGRAM_NAME"]

class DiplomaManagementProfileSerializer(serializers.ModelSerializer):
    academicProgram = AcademicProgram_Serializer(source='ACADEMIC_PROGRAM_ID', many=False)
    class Meta:
        model = diploma_management_profile
        fields = '__all__'