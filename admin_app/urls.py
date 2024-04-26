
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
]   
