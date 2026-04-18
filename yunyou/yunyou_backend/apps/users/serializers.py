"""User serializers for API"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, VisitedAttraction, UserTask


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token with user info"""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class UserSerializer(serializers.ModelSerializer):
    """User detail serializer"""
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'avatar', 'avatar_url', 
                  'role', 'status', 'points', 'bio', 'preferences', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request and obj.avatar.url:
                return request.build_absolute_uri(obj.avatar.url)
        return None


class UserCreateSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'role']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """User update serializer"""
    
    class Meta:
        model = User
        fields = ['email', 'phone', 'bio', 'preferences', 'avatar']


class UserListSerializer(serializers.ModelSerializer):
    """User list serializer for admin"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'status', 'points', 'created_at']


class PasswordChangeSerializer(serializers.Serializer):
    """Password change serializer"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)


class VisitedAttractionSerializer(serializers.ModelSerializer):
    attraction_name = serializers.CharField(source='attraction.name', read_only=True)
    
    class Meta:
        model = VisitedAttraction
        fields = ['id', 'attraction', 'attraction_name', 'rating', 'comment', 'visited_at']
        read_only_fields = ['id', 'visited_at']


class UserTaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserTask
        fields = ['id', 'title', 'description', 'task_type', 'points_reward', 
                  'is_completed', 'completed_at', 'created_at']
        read_only_fields = ['id', 'created_at']
