from rest_framework import serializers
from .models import *






class academic_programSerializer(serializers.ModelSerializer):
    class Meta:
        model = academic_program
        fields = '__all__'


class degreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = degree

##### Authentication Serializers #######
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
class LogoutSerializer(serializers.Serializer):
    pass

#### Status Type Serializers #######
class AcademicLevelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = academic_level_type
        fields = '__all__'
class LearningStatusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = learning_status_type
        fields = '__all__'       


########  Serializers ########
class AcademicIntakeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = academic_intake_session
        fields = '__all__'


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = curriculum
        fields = '__all__'



##### Student Serializers #######
class StudentSerializer(serializers.ModelSerializer):
    academicleveltype = AcademicLevelTypeSerializer(source='ACADEMIC_LEVEL_TYPE_ID', many=False)
    learningstatustype = LearningStatusTypeSerializer(source='LEARNING_STATUS_TYPE_ID', many=False)

    class Meta:
        model = student
        fields = '__all__'