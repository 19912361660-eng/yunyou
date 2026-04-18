"""Backup views"""
import os
import subprocess
import shutil
from datetime import datetime
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import connection
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import BackupRecord, RestoreRecord
from .serializers import BackupRecordSerializer, RestoreRecordSerializer
from apps.users.permissions import IsAdminUser


def get_backup_dir():
    """Get backup directory path"""
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def execute_mysqldump():
    """Execute mysqldump command"""
    db_settings = settings.DATABASES['default']
    backup_dir = get_backup_dir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"yunyou_backup_{timestamp}.sql"
    filepath = os.path.join(backup_dir, filename)
    
    cmd = [
        'mysqldump',
        '-u', db_settings.get('USER', 'root'),
        f"-p{db_settings.get('PASSWORD', '')}",
        '-h', db_settings.get('HOST', 'localhost'),
        '--port', str(db_settings.get('PORT', 3306)),
        '--databases', db_settings['NAME'],
        '--single-transaction',
        '--quick',
        '--lock-tables=false',
        '--result-file', filepath
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
        return filepath, file_size, None
    except subprocess.CalledProcessError as e:
        return None, 0, str(e.stderr)


@extend_schema(tags=['数据备份'])
class BackupViewSet(viewsets.ModelViewSet):
    """Backup viewset"""
    serializer_class = BackupRecordSerializer
    permission_classes = [IsAdminUser]
    queryset = BackupRecord.objects.all()
    
    @extend_schema(summary='创建备份')
    def create(self, request, *args, **kwargs):
        name = request.data.get('name', f"备份_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        backup_type = request.data.get('backup_type', 'full')
        
        record = BackupRecord.objects.create(
            name=name,
            backup_type=backup_type,
            status='running',
            created_by=request.user,
            started_at=timezone.now()
        )
        
        try:
            filepath, file_size, error = execute_mysqldump()
            
            if filepath:
                record.file_path = filepath
                record.file_size = file_size
                record.status = 'completed'
                record.completed_at = timezone.now()
                record.save()
                return Response(BackupRecordSerializer(record).data, status=status.HTTP_201_CREATED)
            else:
                record.status = 'failed'
                record.note = error
                record.completed_at = timezone.now()
                record.save()
                return Response({'error': f'备份失败: {error}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            record.status = 'failed'
            record.note = str(e)
            record.completed_at = timezone.now()
            record.save()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(summary='下载备份文件')
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        record = self.get_object()
        if record.status != 'completed' or not record.file_path:
            return Response({'error': '备份文件不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        if not os.path.exists(record.file_path):
            return Response({'error': '文件已被删除'}, status=status.HTTP_404_NOT_FOUND)
        
        from django.http import FileResponse
        response = FileResponse(open(record.file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(record.file_path)}"'
        return response
    
    @extend_schema(summary='删除备份')
    def destroy(self, request, *args, **kwargs):
        record = self.get_object()
        if record.file_path and os.path.exists(record.file_path):
            os.remove(record.file_path)
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=['数据备份'])
class RestoreViewSet(viewsets.ModelViewSet):
    """Restore viewset"""
    serializer_class = RestoreRecordSerializer
    permission_classes = [IsAdminUser]
    queryset = RestoreRecord.objects.all()
    
    @extend_schema(summary='从备份恢复')
    def create(self, request, *args, **kwargs):
        backup_id = request.data.get('backup_id')
        try:
            backup = BackupRecord.objects.get(id=backup_id, status='completed')
        except BackupRecord.DoesNotExist:
            return Response({'error': '备份不存在或未完成'}, status=status.HTTP_404_NOT_FOUND)
        
        if not backup.file_path or not os.path.exists(backup.file_path):
            return Response({'error': '备份文件不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        record = RestoreRecord.objects.create(
            backup=backup,
            status='running',
            restored_by=request.user,
            started_at=timezone.now()
        )
        
        try:
            db_settings = settings.DATABASES['default']
            
            with connection.cursor() as cursor:
                with open(backup.file_path, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                    for statement in sql_content.split(';'):
                        statement = statement.strip()
                        if statement:
                            cursor.execute(statement)
            
            record.status = 'completed'
            record.completed_at = timezone.now()
            record.save()
            
            return Response({
                'message': '恢复成功',
                'record': RestoreRecordSerializer(record).data
            })
        except Exception as e:
            record.status = 'failed'
            record.note = str(e)
            record.completed_at = timezone.now()
            record.save()
            return Response({'error': f'恢复失败: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['数据统计'])
class DataStatsView(viewsets.ViewSet):
    """Data statistics view"""
    permission_classes = [IsAdminUser]
    
    @extend_schema(summary='获取数据统计')
    def list(self, request):
        from apps.users.models import User
        from apps.attractions.models import Attraction
        from apps.orders.models import Order
        
        stats = {
            'users': {
                'total': User.objects.count(),
                'active': User.objects.filter(status='active').count(),
                'new_today': User.objects.filter(created_at__date=timezone.now().date()).count(),
            },
            'attractions': {
                'total': Attraction.objects.count(),
                'hot': Attraction.objects.filter(is_hot=True).count(),
            },
            'orders': {
                'total': Order.objects.count(),
                'pending': Order.objects.filter(status='pending').count(),
                'completed': Order.objects.filter(status='completed').count(),
                'today_amount': Order.objects.filter(
                    status='completed',
                    created_at__date=timezone.now().date()
                ).aggregate_total('final_amount') or 0,
            },
            'backups': {
                'total': BackupRecord.objects.count(),
                'last': BackupRecord.objects.order_by('-created_at').first().created_at if BackupRecord.objects.exists() else None,
            }
        }
        
        return Response(stats)
