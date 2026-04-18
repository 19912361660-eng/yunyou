"""AI Assistant views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db import transaction
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import ChatSession, ChatMessage
from .serializers import (
    ChatSessionSerializer, ChatSessionListSerializer,
    ChatMessageSerializer, SendMessageSerializer
)


def generate_ai_response(user_message, context=None):
    """Generate AI response using Gemini API"""
    try:
        import google.generativeai as genai
        api_key = settings.GEMINI_API_KEY
        
        if not api_key:
            return "AI服务未配置，请联系管理员设置GEMINI_API_KEY"
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""你是一个智能旅游助手，名叫云游AI。请根据用户的问题提供有用的回答。

用户问题: {user_message}

请用中文回答，提供有用的旅游建议和帮助。"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"抱歉，AI服务暂时不可用: {str(e)}"


@extend_schema(tags=['AI助手'])
class ChatSessionViewSet(viewsets.ModelViewSet):
    """Chat session viewset"""
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ChatSessionListSerializer
        return ChatSessionSerializer
    
    @extend_schema(summary='发送消息')
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        with transaction.atomic():
            if data.get('session_id'):
                session = ChatSession.objects.get(id=data['session_id'], user=request.user)
            else:
                session = ChatSession.objects.create(
                    user=request.user,
                    title=data['message'][:50]
                )
            
            ChatMessage.objects.create(
                session=session,
                message_type='user',
                content=data['message']
            )
            
            ai_response = generate_ai_response(data['message'], session.context)
            
            assistant_msg = ChatMessage.objects.create(
                session=session,
                message_type='assistant',
                content=ai_response
            )
            
            session.updated_at = assistant_msg.created_at
            session.save()
        
        return Response({
            'session': ChatSessionSerializer(session).data,
            'message': ChatMessageSerializer(assistant_msg).data
        })
    
    @extend_schema(summary='获取历史消息')
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        session = self.get_object()
        messages = session.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @extend_schema(summary='清空会话')
    @action(detail=True, methods=['delete'])
    def clear(self, request, pk=None):
        session = self.get_object()
        session.messages.all().delete()
        return Response({'message': '会话已清空'})


@extend_schema(tags=['AI助手'])
class ChatMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """Chat message viewset (read only)"""
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatMessage.objects.filter(session__user=self.request.user)
