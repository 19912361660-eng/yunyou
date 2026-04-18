"""User views for API"""
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import User, VisitedAttraction, UserTask
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    UserListSerializer, CustomTokenObtainPairSerializer,
    PasswordChangeSerializer, VisitedAttractionSerializer, UserTaskSerializer
)
from .permissions import IsAdminUser, IsOwnerOrAdmin

User = get_user_model()


@extend_schema(tags=['认证'])
class CustomTokenObtainPairView(TokenObtainPairView):
    """JWT token obtain view with custom serializer"""
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(tags=['认证'])
class RegisterView(generics.CreateAPIView):
    """User registration"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


@extend_schema(tags=['用户'])
class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile view"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer


@extend_schema(tags=['用户'])
class ChangePasswordView(generics.UpdateAPIView):
    """Change user password"""
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': '旧密码不正确'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': '密码修改成功'})


@extend_schema(tags=['用户管理'])
@extend_schema_view(
    list=extend_schema(summary='用户列表'),
    retrieve=extend_schema(summary='用户详情'),
    create=extend_schema(summary='创建用户'),
    update=extend_schema(summary='更新用户'),
    partial_update=extend_schema(summary='部分更新用户'),
    destroy=extend_schema(summary='删除用户'),
)
class UserManagementViewSet(viewsets.ModelViewSet):
    """Admin user management viewset"""
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['role', 'status']
    search_fields = ['username', 'email', 'phone']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserListSerializer
    
    @extend_schema(summary='切换用户状态')
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        user = self.get_object()
        user.status = 'disabled' if user.status == 'active' else 'active'
        user.save()
        return Response({'status': user.status})
    
    @extend_schema(summary='重置用户密码')
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        from django.contrib.auth.hashers import make_password
        user = self.get_object()
        new_password = request.data.get('password', '123456')
        user.password = make_password(new_password)
        user.save()
        return Response({'message': f'密码已重置为: {new_password}'})
    
    @extend_schema(summary='用户积分管理')
    @action(detail=True, methods=['post'])
    def manage_points(self, request, pk=None):
        user = self.get_object()
        action_type = request.data.get('action', 'set')
        points = int(request.data.get('points', 0))
        
        if action_type == 'add':
            user.points += points
        elif action_type == 'subtract':
            user.points = max(0, user.points - points)
        else:
            user.points = points
        user.save()
        return Response({'points': user.points})


@extend_schema(tags=['用户'])
class VisitedAttractionViewSet(viewsets.ModelViewSet):
    """User visited attractions"""
    serializer_class = VisitedAttractionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return VisitedAttraction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['用户'])
class UserTaskViewSet(viewsets.ModelViewSet):
    """User tasks"""
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserTask.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @extend_schema(summary='完成任务')
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        if not task.is_completed:
            task.is_completed = True
            from django.utils import timezone
            task.completed_at = timezone.now()
            task.save()
            request.user.points += task.points_reward
            request.user.save()
        return Response({'message': '任务完成', 'points_earned': task.points_reward})


@extend_schema(tags=['数据统计'])
class DashboardStatsView(generics.GenericAPIView):
    """Dashboard statistics for admin"""
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(status='active').count()
        total_attractions = 0
        try:
            from apps.attractions.models import Attraction
            total_attractions = Attraction.objects.count()
        except:
            pass
        
        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'total_attractions': total_attractions,
            'system_status': 'running'
        })
