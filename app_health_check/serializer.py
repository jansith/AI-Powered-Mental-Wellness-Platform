from rest_framework import serializers
from .models import *

class ADHDQuestionnaireSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    
    class Meta:
        model = ADHDQuestionnaire
        fields = '__all__'
        read_only_fields = ['adhd_score', 'adhd_risk_level', 'created_at']


class DepressionQuestionnaireSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    
    class Meta:
        model = DepressionQuestionnaire
        fields = '__all__'
        read_only_fields = ['depression_score', 'depression_level', 'recommendation', 'created_at']
