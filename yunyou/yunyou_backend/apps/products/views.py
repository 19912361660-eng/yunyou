"""Product views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.db import transaction
import uuid
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Product, Category, ExchangeRecord
from .serializers import (
    ProductSerializer, ProductListSerializer, CategorySerializer,
    ExchangeRecordSerializer, ExchangeCreateSerializer
)
from apps.users.permissions import IsAdminUser


@extend_schema(tags=['商品分类'])
class CategoryViewSet(viewsets.ModelViewSet):
    """Product category viewset"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
    @extend_schema(summary='获取分类及商品')
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(category=category, status='active')
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


@extend_schema(tags=['商品'])
@extend_schema_view(
    list=extend_schema(summary='商品列表'),
    retrieve=extend_schema(summary='商品详情'),
)
class ProductViewSet(viewsets.ModelViewSet):
    """Product viewset"""
    queryset = Product.objects.filter(status='active')
    permission_classes = [AllowAny]
    filterset_fields = ['category', 'is_featured', 'is_new']
    search_fields = ['name', 'description']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    @extend_schema(summary='精选商品')
    @action(detail=False, methods=['get'])
    def featured(self, request):
        queryset = self.queryset.filter(is_featured=True)[:10]
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(summary='新品上架')
    @action(detail=False, methods=['get'])
    def new(self, request):
        queryset = self.queryset.filter(is_new=True)[:10]
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=['积分兑换'])
class ExchangeRecordViewSet(viewsets.ModelViewSet):
    """Exchange record viewset"""
    serializer_class = ExchangeRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ExchangeRecord.objects.filter(user=self.request.user)
    
    @extend_schema(summary='兑换商品')
    def create(self, request, *args, **kwargs):
        serializer = ExchangeCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        with transaction.atomic():
            record = ExchangeRecord.objects.create(
                record_no = f"EX{uuid.uuid4().hex[:12].upper()}",
                user = request.user,
                product = data['product'],
                points_spent = data['total_points'],
                quantity = data['quantity'],
                address = data['address'],
                contact_name = data['contact_name'],
                contact_phone = data['contact_phone'],
            )
            
            data['product'].stock -= data['quantity']
            data['product'].sold_count += data['quantity']
            data['product'].save()
            
            request.user.points -= data['total_points']
            request.user.save()
        
        return Response(ExchangeRecordSerializer(record).data, status=status.HTTP_201_CREATED)
    
    @extend_schema(summary='确认收货')
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        record = self.get_object()
        if record.status != 'shipped':
            return Response({'error': '订单状态不允许确认收货'}, status=status.HTTP_400_BAD_REQUEST)
        
        record.status = 'completed'
        record.completed_at = timezone.now()
        record.save()
        return Response({'message': '收货成功'})
