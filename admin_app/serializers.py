from rest_framework import serializers
from .models import *





class academic_programSerializer(serializers.ModelSerializer):
    class Meta:
        model = academic_program
        fields = '__all__'


class degreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = degree
        fields = '__all__'