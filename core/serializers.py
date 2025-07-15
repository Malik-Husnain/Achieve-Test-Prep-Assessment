from rest_framework import serializers
from .models import UserProgress

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['course', 'progress']