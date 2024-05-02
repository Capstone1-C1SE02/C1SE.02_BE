from django.urls import path
from .views import *

urlpatterns = [
    path('generate-captcha', GenerateCaptchaAPIView.as_view(), name='generate-captcha'),
    path('informationretrievalthroughtext', InformationRetrievalthroughTextAPIView.as_view(), name='information-retrieval-through-text'),
]