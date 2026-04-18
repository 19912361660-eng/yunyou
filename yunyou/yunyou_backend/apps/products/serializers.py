"""Product serializers"""
from rest_framework import serializers
from .models import Product, Category, ExchangeRecord


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'description']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'description', 'image',
                  'images', 'points', 'price', 'stock', 'sold_count', 'status',
                  'is_featured', 'is_new', 'exchange_rules', 'created_at']


class ProductListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'points', 'price', 'stock', 
                  'is_featured', 'is_new', 'status']


class ExchangeRecordSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    
    class Meta:
        model = ExchangeRecord
        fields = ['id', 'record_no', 'product', 'product_name', 'product_image',
                  'points_spent', 'quantity', 'status', 'address', 'contact_name',
                  'contact_phone', 'tracking_no', 'shipped_at', 'completed_at', 'created_at']


class ExchangeCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
    address = serializers.CharField()
    contact_name = serializers.CharField()
    contact_phone = serializers.CharField()
    
    def validate(self, data):
        user = self.context['request'].user
        product = Product.objects.get(id=data['product_id'])
        
        if product.stock < data['quantity']:
            raise serializers.ValidationError("库存不足")
        
        total_points = product.points * data['quantity']
        if user.points < total_points:
            raise serializers.ValidationError("积分不足")
        
        data['product'] = product
        data['total_points'] = total_points
        return data
