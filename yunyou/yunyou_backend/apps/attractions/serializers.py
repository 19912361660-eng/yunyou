"""Attraction serializers"""
from rest_framework import serializers
from .models import Attraction, AttractionImage, Route, RouteDay, RouteAttraction, AttractionLike
from apps.users.serializers import UserSerializer


class AttractionImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AttractionImage
        fields = ['id', 'image', 'caption', 'order']


class AttractionSerializer(serializers.ModelSerializer):
    images = serializers.JSONField(required=False)
    tags = serializers.JSONField(required=False)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Attraction
        fields = ['id', 'name', 'location', 'province', 'city', 'description', 
                  'detailed_description', 'image', 'images', 'rating', 'rating_count',
                  'tags', 'category', 'price', 'opening_hours', 'address', 'latitude',
                  'longitude', 'phone', 'website', 'is_recommended', 'is_hot',
                  'visit_duration', 'facilities', 'traffic_info', 'view_count', 
                  'like_count', 'status', 'is_liked', 'created_at', 'updated_at']
        read_only_fields = ['id', 'rating', 'rating_count', 'view_count', 'like_count', 'created_at']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return AttractionLike.objects.filter(user=request.user, attraction=obj).exists()
        return False


class AttractionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    
    class Meta:
        model = Attraction
        fields = ['id', 'name', 'location', 'image', 'rating', 'rating_count',
                  'tags', 'price', 'is_recommended', 'is_hot']


class AttractionCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attraction
        fields = ['name', 'location', 'province', 'city', 'description', 
                  'detailed_description', 'image', 'images', 'tags', 'category',
                  'price', 'opening_hours', 'address', 'latitude', 'longitude',
                  'phone', 'website', 'is_recommended', 'is_hot', 'visit_duration',
                  'facilities', 'traffic_info', 'status']
    
    def validate_tags(self, value):
        if isinstance(value, list):
            return value
        return []


class RouteAttractionSerializer(serializers.ModelSerializer):
    attraction = AttractionListSerializer(read_only=True)
    attraction_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = RouteAttraction
        fields = ['id', 'attraction', 'attraction_id', 'order', 'arrival_time',
                  'departure_time', 'visit_duration', 'notes', 'transportation']


class RouteDaySerializer(serializers.ModelSerializer):
    attractions = RouteAttractionSerializer(source='routeattraction_set', many=True, read_only=True)
    
    class Meta:
        model = RouteDay
        fields = ['id', 'day_number', 'date', 'title', 'notes', 'attractions']


class RouteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    days = RouteDaySerializer(source='routeday_set', many=True, read_only=True)
    days_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Route
        fields = ['id', 'user', 'title', 'description', 'start_date', 'end_date',
                  'total_days', 'estimated_cost', 'status', 'is_public', 
                  'like_count', 'share_count', 'days', 'days_count', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'like_count', 'share_count', 'created_at']
    
    def get_days_count(self, obj):
        return obj.days.count()


class RouteCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Route
        fields = ['title', 'description', 'start_date', 'end_date', 'status', 'is_public']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        route = super().create(validated_data)
        route.total_days = (route.end_date - route.start_date).days + 1 if route.start_date and route.end_date else 1
        route.save()
        return route


class RouteListSerializer(serializers.ModelSerializer):
    """Lightweight route serializer"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Route
        fields = ['id', 'user', 'title', 'start_date', 'end_date', 'total_days',
                  'estimated_cost', 'like_count', 'share_count', 'created_at']
