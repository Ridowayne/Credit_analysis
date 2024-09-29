from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer as BaseUserSerializer
from .models import Buyer_Analysis
from .models import CustomUser

class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'username', 'password', 'phone_number', 'staff_id', 'role']
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            staff_id=validated_data.get('staff_id'),
            role=validated_data.get('role'))
        
        return user

class BuyerAnalysisSerializer(serializers.Serializer):
    class Meta:
        model = Buyer_Analysis
        fields = ['name', 'submitedat', 'completed', 'updatedat', 'worthy', 'user', 'phone_number', 'bank_name', 'bank_statement']

