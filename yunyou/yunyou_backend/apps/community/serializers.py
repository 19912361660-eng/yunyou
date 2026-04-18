"""Community serializers"""
from rest_framework import serializers
from .models import Post, Comment, PostLike, CommentLike
from apps.users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'parent', 'like_count', 'replies', 'created_at']
    
    def get_replies(self, obj):
        if obj.parent is None:
            replies = Comment.objects.filter(parent=obj, is_deleted=False)
            return CommentSerializer(replies, many=True, context=self.context).data
        return []


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'post_type', 'title', 'content', 'images',
                  'attraction', 'view_count', 'like_count', 'comment_count',
                  'is_pinned', 'comments', 'created_at', 'updated_at']
    
    def get_comments(self, obj):
        top_comments = Comment.objects.filter(post=obj, parent=None, is_deleted=False)[:5]
        return CommentSerializer(top_comments, many=True, context=self.context).data


class PostListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'post_type', 'title', 'images', 'view_count',
                  'like_count', 'comment_count', 'is_pinned', 'created_at']


class CommentCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['post', 'content', 'parent']
    
    def create(self, validated_data):
        comment = super().create(validated_data)
        comment.post.comment_count += 1
        comment.post.save()
        return comment
