"""Attraction views for API"""
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Attraction, Route, RouteDay, RouteAttraction, AttractionLike
from .serializers import (
    AttractionSerializer, AttractionListSerializer, AttractionCreateUpdateSerializer,
    RouteSerializer, RouteCreateSerializer, RouteListSerializer,
    RouteDaySerializer, RouteAttractionSerializer
)
from apps.users.permissions import IsAdminUser


@extend_schema(tags=['景点'])
@extend_schema_view(
    list=extend_schema(summary='景点列表'),
    retrieve=extend_schema(summary='景点详情'),
)
class AttractionViewSet(viewsets.ModelViewSet):
    """Attraction viewset"""
    queryset = Attraction.objects.filter(status='active')
    permission_classes = [AllowAny]
    filterset_fields = ['province', 'city', 'category', 'is_recommended', 'is_hot']
    search_fields = ['name', 'location', 'description', 'tags']
    ordering_fields = ['rating', 'view_count', 'like_count', 'price', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AttractionListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return AttractionCreateUpdateSerializer
        return AttractionSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @extend_schema(summary='获取推荐景点')
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        queryset = self.queryset.filter(is_recommended=True)[:10]
        serializer = AttractionListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(summary='获取热门景点')
    @action(detail=False, methods=['get'])
    def hot(self, request):
        queryset = self.queryset.filter(is_hot=True)[:10]
        serializer = AttractionListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(summary='搜索景点')
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        province = request.query_params.get('province', '')
        city = request.query_params.get('city', '')
        
        queryset = self.queryset
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(tags__icontains=query)
            )
        if province:
            queryset = queryset.filter(province=province)
        if city:
            queryset = queryset.filter(city=city)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AttractionListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = AttractionListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(summary='点赞景点')
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        attraction = self.get_object()
        like, created = AttractionLike.objects.get_or_create(
            user=request.user, 
            attraction=attraction
        )
        if not created:
            like.delete()
            attraction.like_count = max(0, attraction.like_count - 1)
            attraction.save()
            return Response({'liked': False, 'like_count': attraction.like_count})
        
        attraction.like_count += 1
        attraction.save()
        return Response({'liked': True, 'like_count': attraction.like_count})


@extend_schema(tags=['路线'])
class RouteViewSet(viewsets.ModelViewSet):
    """Route viewset"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Route.objects.all()
        return Route.objects.filter(
            Q(user=self.request.user) | Q(is_public=True)
        )
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RouteCreateSerializer
        if self.action == 'list':
            return RouteListSerializer
        return RouteSerializer
    
    @extend_schema(summary='分享路线')
    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        route = self.get_object()
        route.is_public = True
        route.status = 'shared'
        route.share_count += 1
        route.save()
        return Response({'message': '路线已分享'})
    
    @extend_schema(summary='点赞路线')
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        route = self.get_object()
        route.like_count += 1
        route.save()
        return Response({'like_count': route.like_count})
    
    @extend_schema(summary='获取公开路线')
    @action(detail=False, methods=['get'])
    def public_routes(self, request):
        queryset = Route.objects.filter(is_public=True)[:20]
        serializer = RouteListSerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=['路线'])
class RouteDayViewSet(viewsets.ModelViewSet):
    """Route day management"""
    serializer_class = RouteDaySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return RouteDay.objects.filter(
            route__user=self.request.user
        )


@extend_schema(tags=['路线'])
class RouteAttractionViewSet(viewsets.ModelViewSet):
    """Route attraction management"""
    serializer_class = RouteAttractionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return RouteAttraction.objects.filter(
            route_day__route__user=self.request.user
        )
