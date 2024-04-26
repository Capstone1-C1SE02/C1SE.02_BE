
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [

    path('academic_program/', academic_programList.as_view()),
    path('academic_program/<int:pk>/', academic_programDetail.as_view()),

    path('degree/', degreeList.as_view()),
    path('degree/<int:pk>/', degreeDetail.as_view()),

    ### Authentication URLs##############
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    ### Status Type  URLs##############
    path('academicleveltype', AcademicLevelTypeList.as_view()),
    path('academicleveltype/<int:pk>', AcademicIntakeSessionDetail.as_view()),
    path('learningstatustype', LearningStatusTypeList.as_view()),
    path('learningstatustype/<int:pk>', LearningStatusTypeDetail.as_view()),


    ### Academic Intake Session URLs##############
    path('academicintakesession', AcademicIntakeSessionList.as_view()),
    path('academicintakesession/<int:pk>', AcademicIntakeSessionDetail.as_view()),
    

    ### Curriculum URLs##############
    path('curriculum', CurriculumList.as_view()),
    path('curriculum/<int:pk>', CurriculumDetail.as_view()),

    
    #### Student URLs##############
    path('student', StudentList.as_view()),
    path('student/<int:pk>', StudentDetail.as_view()),


]   
