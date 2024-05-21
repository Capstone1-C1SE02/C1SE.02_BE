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
    academicProgram = PostAcademicProgramSerializer(source='ACADEMIC_PROGRAM_ID', many=False)
    class Meta:
        model = curriculum
        fields = '__all__'

class PostCurriculumSerializer(serializers.ModelSerializer):
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
        fields = '__all__'



####### AcademicIntakeSession_AcademicProgram_Curriculum_Serializers #######
class  AcademicIntakeSession_Serializer(serializers.ModelSerializer):
    class Meta:
        model = academic_intake_session
        fields = ["ACADEMIC_INTAKE_SESSION_ID","ACADEMIC_INTAKE_SESSION_NAME"]

class AcademicProgram_Serializer(serializers.ModelSerializer):
    class Meta:
        model = academic_program
        fields = ["ACADEMIC_PROGRAM_ID","ACADEMIC_PROGRAM_NAME"]

class Curriculum_Serializer(serializers.ModelSerializer):
    class Meta:
        model = curriculum
        fields = ["CURRICULUM_ID","CURRICULUM_NAME"]

class Get_AcademicIntakeSession_AcademicProgram_Curriculum_Serializers(serializers.ModelSerializer):
    academic_intake_session = AcademicIntakeSession_Serializer(source='ACADEMIC_INTAKE_SESSION_ID', many=False)
    academic_program = AcademicProgram_Serializer(source='ACADEMIC_PROGRAM_ID', many=False)
    curriculum = Curriculum_Serializer(source='CURRICULUM_ID', many=False)
    class Meta:
        model = academic_intake_session_academic_program_curriculum
        fields = '__all__'

class Post_AcademicIntakeSession_AcademicProgram_Curriculum_Serializers(serializers.ModelSerializer):
    class Meta:
        model = academic_intake_session_academic_program_curriculum
        fields = '__all__'

###### Student_AcademicIntakeSession_AcademicProgramSerializers #######
class Student_Serializer(serializers.ModelSerializer):
    class Meta:
        model = student
        fields = ["STUDENT_ID_NUMBER"]

class Get_Student_AcademicIntakeSession_AcademicProgram_Serializers(serializers.ModelSerializer):
    student = Student_Serializer(source='STUDENT_ID_NUMBER', many=False)
    academic_intake_session = AcademicIntakeSession_Serializer(source='ACADEMIC_INTAKE_SESSION_ID', many=False)
    academic_program = AcademicProgram_Serializer(source='ACADEMIC_PROGRAM_ID', many=False)
    class Meta:
        model = student_academic_intake_session_academic_program
        fields = '__all__'

class Post_Student_AcademicIntakeSession_AcademicProgram_Serializers(serializers.ModelSerializer):
    class Meta:
        model = student_academic_intake_session_academic_program
        fields = '__all__'


##### DiplomaManagementProfileSerializers #######
class GetDiplomaManagementProfileSerializer(serializers.ModelSerializer):
    academicProgram = AcademicProgram_Serializer(source='ACADEMIC_PROGRAM_ID', many=False)
    class Meta:
        model = diploma_management_profile
        fields = '__all__'
        
class PostDiplomaManagementProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = diploma_management_profile
        fields = '__all__'