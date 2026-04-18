"""Community models"""
from django.db import models
from django.conf import settings


class Post(models.Model):
    """Community post model"""
    
    POST_TYPE_CHOICES = [
        ('share', '分享'),
        ('question', '问答'),
        ('guide', '攻略'),
        ('notice', '公告'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField('类型', max_length=20, choices=POST_TYPE_CHOICES, default='share')
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    images = models.JSONField('图片', default=list, blank=True)
    attraction = models.ForeignKey('attractions.Attraction', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    view_count = models.IntegerField('浏览次数', default=0)
    like_count = models.IntegerField('点赞数', default=0)
    comment_count = models.IntegerField('评论数', default=0)
    is_pinned = models.BooleanField('置顶', default=False)
    is_deleted = models.BooleanField('已删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'community_posts'
        ordering = ['-is_pinned', '-created_at']


class Comment(models.Model):
    """Post comment model"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField('内容')
    like_count = models.IntegerField('点赞数', default=0)
    is_deleted = models.BooleanField('已删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        db_table = 'community_comments'
        ordering = ['created_at']


class PostLike(models.Model):
    """Post like model"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField('时间', auto_now_add=True)
    
    class Meta:
        db_table = 'post_likes'
        unique_together = ['user', 'post']


class CommentLike(models.Model):
    """Comment like model"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField('时间', auto_now_add=True)
    
    class Meta:
        db_table = 'comment_likes'
        unique_together = ['user', 'comment']
