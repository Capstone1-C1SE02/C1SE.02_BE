from rest_framework import serializers
from .models import *




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


########  Academic Intake Session Serializers ########
class AcademicIntakeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = academic_intake_session
        fields = '__all__'


################# Degree Serializers ################
class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = degree
        fields = '__all__'


################# Academic Program Serializers ################
class GetAcademicProgramSerializer(serializers.ModelSerializer):
    academicleveltype = AcademicLevelTypeSerializer(source='ACADEMIC_LEVEL_TYPE_ID', many=False)
    degree_item = DegreeSerializer(source='DEGREE_ID', many=False)
    class Meta:
        model = academic_program
        fields = '__all__'

class PostAcademicProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = academic_program
        fields = '__all__'

########  Curriculum Serializer ########

class GetCurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = curriculum
        fields = '__all__'

class PostCurriculumSerializer(serializers.ModelSerializer):
    academicProgram = PostAcademicProgramSerializer(source='ACADEMIC_PROGRAM_ID', many=False)
    class Meta:
        model = curriculum
        fields = '__all__'


##### Student Serializers #######
class GetStudentSerializer(serializers.ModelSerializer):
    academicleveltype = AcademicLevelTypeSerializer(source='ACADEMIC_LEVEL_TYPE_ID', many=False)
    learningstatustype = LearningStatusTypeSerializer(source='LEARNING_STATUS_TYPE_ID', many=False)

    class Meta:
        model = student
        fields = '__all__'

class PostStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = student
