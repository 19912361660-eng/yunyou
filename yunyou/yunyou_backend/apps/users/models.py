"""User models for 云游智行"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role-based access control"""
    
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('user', '普通用户'),
    ]
    STATUS_CHOICES = [
        ('active', '活跃'),
        ('disabled', '禁用'),
    ]
    
    phone = models.CharField('手机号', max_length=20, blank=True, null=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES, default='user')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='active')
    points = models.IntegerField('积分', default=0)
    bio = models.TextField('个人简介', blank=True)
    preferences = models.JSONField('偏好设置', default=dict, blank=True)
    visited_attractions = models.ManyToManyField(
        'attractions.Attraction', 
        through='users.VisitedAttraction',
        related_name='visitors',
        blank=True
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户管理'
    
    def __str__(self):
        return self.username


class VisitedAttraction(models.Model):
    """User visited attractions with rating"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visit_records')
    attraction = models.ForeignKey('attractions.Attraction', on_delete=models.CASCADE)
    rating = models.IntegerField('评分', choices=[(i, i) for i in range(1, 6)], null=True)
    comment = models.TextField('评论', blank=True)
    visited_at = models.DateTimeField('访问时间', auto_now_add=True)
    
    class Meta:
        db_table = 'user_visited_attractions'
        unique_together = ['user', 'attraction']


class UserTask(models.Model):
    """User tasks for gamification"""
    TASK_TYPE_CHOICES = [
        ('daily', '每日任务'),
        ('achievement', '成就任务'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField('任务名称', max_length=100)
    description = models.TextField('任务描述')
    task_type = models.CharField('任务类型', max_length=20, choices=TASK_TYPE_CHOICES)
    points_reward = models.IntegerField('积分奖励', default=0)
    is_completed = models.BooleanField('是否完成', default=False)
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        db_table = 'user_tasks'
        ordering = ['-created_at']
