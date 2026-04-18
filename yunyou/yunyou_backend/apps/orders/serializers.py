"""Order serializers"""
from rest_framework import serializers
from .models import Order, OrderItem
from apps.users.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ['id', 'item_type', 'item_id', 'item_name', 'quantity', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_no', 'user', 'order_type', 'status', 'total_amount',
                  'points_used', 'points_discount', 'final_amount', 'payment_method',
                  'payment_time', 'contact_name', 'contact_phone', 'note', 'items',
                  'created_at', 'updated_at']


class OrderListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['id', 'order_no', 'order_type', 'status', 'final_amount',
                  'payment_time', 'contact_name', 'created_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(write_only=True)
    
    class Meta:
        model = Order
        fields = ['order_type', 'contact_name', 'contact_phone', 'note', 'items']
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("订单商品不能为空")
        return value
    
    def create(self, validated_data):
        import uuid
        items_data = validated_data.pop('items')
        validated_data['order_no'] = f"YY{uuid.uuid4().hex[:12].upper()}"
        validated_data['user'] = self.context['request'].user
        
        total = sum(item['subtotal'] for item in items_data)
        validated_data['total_amount'] = total
        validated_data['final_amount'] = total
        
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order
