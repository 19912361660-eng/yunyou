"""Backup models"""
from django.db import models
from django.conf import settings


class BackupRecord(models.Model):
    """Database backup record"""
    
    BACKUP_TYPE_CHOICES = [
        ('full', '完整备份'),
        ('incremental', '增量备份'),
    ]
    
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('running', '进行中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]
    
    name = models.CharField('备份名称', max_length=200)
    backup_type = models.CharField('备份类型', max_length=20, choices=BACKUP_TYPE_CHOICES, default='full')
    file_path = models.CharField('文件路径', max_length=500, blank=True)
    file_size = models.BigIntegerField('文件大小(bytes)', default=0)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField('备注', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    started_at = models.DateTimeField('开始时间', null=True, blank=True)
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        db_table = 'backup_records'
        ordering = ['-created_at']


class RestoreRecord(models.Model):
    """Database restore record"""
    
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('running', '进行中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]
    
    backup = models.ForeignKey(BackupRecord, on_delete=models.CASCADE, related_name='restores')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField('备注', blank=True)
    restored_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    started_at = models.DateTimeField('开始时间', null=True, blank=True)
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        db_table = 'restore_records'
        ordering = ['-created_at']
