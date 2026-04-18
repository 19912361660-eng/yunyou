"""AI Assistant models"""
from django.db import models
from django.conf import settings


class ChatSession(models.Model):
    """AI chat session"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_sessions')
    title = models.CharField('会话标题', max_length=200, blank=True)
    context = models.JSONField('上下文', default=dict)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'ai_chat_sessions'
        ordering = ['-updated_at']


class ChatMessage(models.Model):
    """AI chat message"""
    
    MESSAGE_TYPE_CHOICES = [
        ('user', '用户'),
        ('assistant', '助手'),
        ('system', '系统'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField('消息类型', max_length=20, choices=MESSAGE_TYPE_CHOICES)
    content = models.TextField('内容')
    metadata = models.JSONField('元数据', default=dict, blank=True)
    created_at = models.DateTimeField('时间', auto_now_add=True)
    
    class Meta:
        db_table = 'ai_chat_messages'
        ordering = ['created_at']
