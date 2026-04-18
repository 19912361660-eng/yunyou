"""Backup serializers"""
from rest_framework import serializers
from .models import BackupRecord, RestoreRecord


class BackupRecordSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = BackupRecord
        fields = ['id', 'name', 'backup_type', 'file_path', 'file_size', 'status',
                  'note', 'created_by', 'created_by_name', 'started_at', 
                  'completed_at', 'created_at']
        read_only_fields = ['id', 'created_at']


class RestoreRecordSerializer(serializers.ModelSerializer):
    restored_by_name = serializers.CharField(source='restored_by.username', read_only=True)
    backup_name = serializers.CharField(source='backup.name', read_only=True)
    
    class Meta:
        model = RestoreRecord
        fields = ['id', 'backup', 'backup_name', 'status', 'note',
                  'restored_by', 'restored_by_name', 'started_at',
                  'completed_at', 'created_at']
