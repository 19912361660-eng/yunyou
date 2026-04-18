"""Community views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Post, Comment, PostLike, CommentLike
from .serializers import PostSerializer, PostListSerializer, CommentSerializer, CommentCreateSerializer
from apps.users.permissions import IsAdminUser


@extend_schema(tags=['社区'])
@extend_schema_view(
    list=extend_schema(summary='帖子列表'),
    retrieve=extend_schema(summary='帖子详情'),
    create=extend_schema(summary='发布帖子'),
)
class PostViewSet(viewsets.ModelViewSet):
    """Post viewset"""
    queryset = Post.objects.filter(is_deleted=False)
    permission_classes = [AllowAny]
    filterset_fields = ['post_type', 'is_pinned']
    search_fields = ['title', 'content']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(summary='我的帖子')
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_posts(self, request):
        posts = self.queryset.filter(user=request.user)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    
    @extend_schema(summary='点赞帖子')
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            like.delete()
            post.like_count = max(0, post.like_count - 1)
            post.save()
            return Response({'liked': False, 'like_count': post.like_count})
        
        post.like_count += 1
        post.save()
        return Response({'liked': True, 'like_count': post.like_count})


@extend_schema(tags=['评论'])
class CommentViewSet(viewsets.ModelViewSet):
    """Comment viewset"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Comment.objects.filter(is_deleted=False)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer
    
    @extend_schema(summary='点赞评论')
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        
        if not created:
            like.delete()
            comment.like_count = max(0, comment.like_count - 1)
            comment.save()
            return Response({'liked': False, 'like_count': comment.like_count})
        
        comment.like_count += 1
        comment.save()
        return Response({'liked': True, 'like_count': comment.like_count})
    
    @extend_schema(summary='删除评论')
    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        comment = self.get_object()
        if comment.user != request.user and request.user.role != 'admin':
            return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)
        
        comment.is_deleted = True
        comment.save()
        comment.post.comment_count = max(0, comment.post.comment_count - 1)
        comment.post.save()
        return Response({'message': '删除成功'})
