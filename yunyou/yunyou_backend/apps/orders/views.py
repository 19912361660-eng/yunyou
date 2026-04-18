"""Order views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Order
from .serializers import OrderSerializer, OrderListSerializer, OrderCreateSerializer
from apps.users.permissions import IsAdminUser


@extend_schema(tags=['订单'])
@extend_schema_view(
    list=extend_schema(summary='订单列表'),
    retrieve=extend_schema(summary='订单详情'),
    create=extend_schema(summary='创建订单'),
)
class OrderViewSet(viewsets.ModelViewSet):
    """Order viewset"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action == 'list':
            return OrderListSerializer
        return OrderSerializer
    
    @extend_schema(summary='支付订单')
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({'error': '订单状态不允许支付'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'paid'
        order.payment_time = timezone.now()
        order.payment_method = request.data.get('method', 'wechat')
        order.save()
        return Response({'message': '支付成功', 'order_no': order.order_no})
    
    @extend_schema(summary='取消订单')
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['pending', 'paid']:
            return Response({'error': '订单状态不允许取消'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'cancelled'
        order.save()
        return Response({'message': '订单已取消'})
    
    @extend_schema(summary='申请退款')
    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        order = self.get_object()
        if order.status != 'paid':
            return Response({'error': '订单状态不允许退款'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'refunded'
        order.save()
        return Response({'message': '退款申请已提交'})
    
    @extend_schema(summary='确认完成')
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def complete(self, request, pk=None):
        order = self.get_object()
        order.status = 'completed'
        order.save()
        return Response({'message': '订单已完成'})
