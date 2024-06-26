
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    ### Authentication URLs##############
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    ### Status Type  URLs##############
    path('academicleveltype/', AcademicLevelTypeList.as_view()),
    path('academicleveltype/<int:pk>', AcademicIntakeSessionDetail.as_view()),
    path('learningstatustype/', LearningStatusTypeList.as_view()),
    path('learningstatustype/<int:pk>', LearningStatusTypeDetail.as_view()),

    ### Academic Intake Session URLs##############
    path('academicintakesession/', AcademicIntakeSessionList.as_view(),name='academic-intake-session-list'),
    path('academicintakesession/<int:pk>', AcademicIntakeSessionDetail.as_view(),name='academic-intake-session-id'),
    

    ### Curriculum URLs##############
    path('curriculum/', CurriculumList.as_view(),name='curriculum-list'),
    path('curriculum/<int:pk>', CurriculumDetail.as_view(),name='curriculum-id'),

    #### Student URLs##############
    path('student/', StudentList.as_view(),name='student-list'),
    path('student/<int:pk>', StudentDetail.as_view(),name='student-id'),

    ### Degree URLs##############
    path('degree/', DegreeList.as_view(), name='degree-list'),
    path('degree/<int:pk>', DegreeDetail.as_view(),name='degree-id'),

    ### Academic Program URLs##############
    path('academicprogram/', AcademicProgramList.as_view(),name='academic-program-list'),
    path('academicprogram/<int:pk>', AcademicProgramDetail.as_view(),name='academic-program-id'),

    ### Academic Intake Session Academic Program Curriculum URLs##############
    path('academicintakesessionacademicprogramcurriculum/', AcademicIntakeSession_AcademicProgram_Curriculum_List.as_view(),name='AISAPC-list'),
    path('academicintakesessionacademicprogramcurriculum/<int:pk>', AcademicIntakeSession_AcademicProgram_Curriculum_Detail.as_view(),name='AISAPC-id'),

    ### Student Academic Intake Session Academic Program URLs##############
    path('studentacademicintakesessionacademicprogram', Student_AcademicIntakeSession_AcademicProgram_List.as_view(),name='SAISAP-list'),
    path('studentacademicintakesessionacademicprogram/<int:pk>', Student_AcademicIntakeSession_AcademicProgram_Detail.as_view(),name='SAISAP-id'),

    ### Diploma Management Profile URLs ############## 
    path('diplomamanagementprofile/', DiplomaManagementProfileList.as_view(),name='Diploma-list'),
    path('diplomamanagementprofile/<int:pk>', DiplomaManagementProfileDetail.as_view(),name='Diploma-id'),

    ### Search URLs ##############
    path('search/student', SearchStudent.as_view()),
    path('search/degree', SearchDegree.as_view()),
    path('search/academicprogram', SearchAcademicProgram.as_view()),
    path('search/curriculum', SearchCurriculum.as_view()),


    ### Excel Upload URLs ##############
    path('upload-student', UploadStudentExcel.as_view(), name='upload_student_excel'),
    path('upload-diploma', UploadDiplomaExcel.as_view(), name='upload-diploma'),

]   
