from django.db import models
from django.contrib.auth.models import AbstractUser

class academic_intake_session(models.Model):
    ACADEMIC_INTAKE_SESSION_ID = models.AutoField(primary_key=True)
    ACADEMIC_INTAKE_SESSION_NAME = models.CharField(max_length=50,null= False)
    START_DATE = models.DateField(null= False)

class degree(models.Model):
    DEGREE_ID = models.AutoField(primary_key=True,null= False)
    DEGREE_NAME = models.CharField(max_length=50,null= False)
    DEGREE_CODE = models.CharField(max_length=20,null= False)
    DEGREE_STATUS = models.CharField(max_length=50,null= False)
    DESCRIPTON = models.CharField(max_length=255,null= False)

class academic_level_type(models.Model):
    ACADEMIC_LEVEL_TYPE_ID = models.AutoField(primary_key=True)
    ACADEMIC_LEVEL_TYPE_NAME = models.CharField(max_length=50,null= False) 

class academic_program(models.Model):
    ACADEMIC_PROGRAM_ID = models.AutoField(primary_key=True)
    ACADEMIC_PROGRAM_CODE = models.CharField(max_length=20,null= False)
    ACADEMIC_PROGRAM_NAME = models.CharField(max_length=50,null= False)
    MODE_OF_STUDY = models.CharField(max_length=50,null= False)
    DEGREE_DURATION = models.CharField(max_length=50,null= False)
    DESCRIPTION = models.CharField(max_length=255,null= False)
    ACADEMIC_LEVEL_TYPE_ID = models.ForeignKey(academic_level_type, on_delete = models.CASCADE, to_field = 'ACADEMIC_LEVEL_TYPE_ID')
    DEGREE_ID = models.ForeignKey(degree, on_delete = models.CASCADE, to_field = 'DEGREE_ID')

class curriculum(models.Model):
    CURRICULUM_ID = models.AutoField(primary_key=True)
    CURRICULUM_NAME = models.CharField(max_length=50,null= False)
    DESCRIPTION = models.CharField(max_length=255,null= False)
    CURRICULUM_STATUS_NAME = models.BooleanField(default=True)
    ACADEMIC_PROGRAM_ID = models.ForeignKey(academic_program, on_delete = models.CASCADE, to_field = 'ACADEMIC_PROGRAM_ID')

class academic_intake_session_academic_program_curriculum(models.Model):
    ACADEMIC_INTAKE_SESSION_ID = models.ForeignKey(academic_intake_session, on_delete = models.CASCADE, to_field = 'ACADEMIC_INTAKE_SESSION_ID')
    ACADEMIC_PROGRAM_ID = models.ForeignKey(academic_program, on_delete = models.CASCADE, to_field = 'ACADEMIC_PROGRAM_ID')
    CURRICULUM_ID = models.ForeignKey(curriculum, on_delete = models.CASCADE, to_field = 'CURRICULUM_ID')
    STATUS_NAME = models.CharField(max_length=50,default = True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ACADEMIC_INTAKE_SESSION_ID', 'ACADEMIC_PROGRAM_ID', 'CURRICULUM_ID'], name='PK_intake_session_program_curriculum')
        ]

class learning_status_type(models.Model):
    LEARNING_STATUS_TYPE_ID = models.AutoField(primary_key=True)
    LEARNING_STATUS_TYPE_NAME = models.CharField(max_length=50,null= False)

class student(models.Model):
    STUDENT_ID_NUMBER = models.CharField(max_length=50,null= False,primary_key=True)
    LAST_NAME = models.CharField(max_length=20,null= False)
    FIRST_NAME = models.CharField(max_length=20,null= False)
    MIDDLE_NAME = models.CharField(max_length=20,null= False)
    GENDER = models.BooleanField()
    BIRTH_DATE = models.DateField(null=False)
    BIRTH_PLACE = models.CharField(max_length=100,null=False)
    PEOPLE_ID_NUMBER = models.CharField(max_length=50,null= False)
    NATION = models.CharField(max_length=50,null= False)
    NATIONALITY = models.CharField(max_length=50,null= False)
    PHONE_NUMBER = models.CharField(max_length=50,null = True) 
    EMAIL = models.CharField(max_length=50,null = True)
    COMMENTS = models.CharField(max_length=255,null= False)
    LEARNING_STATUS_TYPE_ID = models.CharField(max_length=50,null= False)
    ACADEMIC_LEVEL_TYPE_ID = models.ForeignKey(academic_level_type, on_delete = models.CASCADE, to_field = 'ACADEMIC_LEVEL_TYPE_ID')

class student_academic_intake_session_academic_program(models.Model):
    STUDENT_ID_NUMBER = models.ForeignKey(student, on_delete = models.CASCADE, to_field = 'STUDENT_ID_NUMBER')
    ACADEMIC_INTAKE_SESSION_ID = models.ForeignKey(academic_intake_session, on_delete = models.CASCADE, to_field = 'ACADEMIC_INTAKE_SESSION_ID')
    ACADEMIC_PROGRAM_ID = models.ForeignKey(academic_program, on_delete = models.CASCADE, to_field = 'ACADEMIC_PROGRAM_ID')
    LEARNING_STATUS_TYPE_ID = models.ForeignKey(learning_status_type, on_delete = models.CASCADE, to_field = 'LEARNING_STATUS_TYPE_ID')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['STUDENT_ID_NUMBER', 'ACADEMIC_INTAKE_SESSION_ID', 'ACADEMIC_PROGRAM_ID'], name='PK_student_c_intake_session_program')
        ]


class account(AbstractUser):
    ACCOUNT_ID = models.AutoField(primary_key=True)
    MIDDLE_NAME = models.CharField(max_length=20,null= False)

    def id(self):
        return self.ACCOUNT_ID

class diploma_management_profile(models.Model):
    DIPLOMA_MANAGEMENT_PROFILE_ID = models.AutoField(primary_key=True)
    STUDENT_ID_NUMBER = models.ForeignKey(student, on_delete = models.CASCADE, to_field = 'STUDENT_ID_NUMBER')
    ACADEMIC_PROGRAM_ID = models.ForeignKey(academic_program, on_delete = models.CASCADE, to_field = 'ACADEMIC_PROGRAM_ID')
    GRADUATION_YEAR = models.CharField(max_length=20,null= False)
    MODE_OF_STUDY = models.CharField(max_length=50,null= False)
    CLASSIFIED_BY_ACADEMIC_RECORDS = models.CharField(max_length=50,null= False)
    CERTIFICATE_NUMBER = models.CharField(max_length=50,null= False)
    NUMBER_ENTERED_INTO_THE_DEGREE_TRACKING_BOOK = models.CharField(max_length=50,null= False)
    DATE_OF_DECISION_ANNOUNCEMENT = models.DateField(null= False)
    COMMENT = models.CharField(max_length=255,null= False)
    DATE_UPDATED = models.DateField(null= False)
    ACCOUNT_ID = models.ForeignKey(account, on_delete = models.CASCADE, to_field = 'ACCOUNT_ID')

   