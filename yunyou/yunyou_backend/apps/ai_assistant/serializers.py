"""AI Assistant serializers"""
from rest_framework import serializers
from .models import ChatSession, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'message_type', 'content', 'metadata', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(source='chatmessage_set', many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'context', 'messages', 'last_message', 'created_at', 'updated_at']
    
    def get_last_message(self, obj):
        last = obj.messages.order_by('-created_at').first()
        if last:
            return ChatMessageSerializer(last).data
        return None


class ChatSessionListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'last_message', 'created_at', 'updated_at']
    
    def get_last_message(self, obj):
        last = obj.messages.order_by('-created_at').first()
        if last:
            return {
                'content': last.content[:100],
                'message_type': last.message_type,
                'created_at': last.created_at
            }
        return None


class SendMessageSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=False)
    message = serializers.CharField()
    context = serializers.JSONField(required=False, default=dict)
