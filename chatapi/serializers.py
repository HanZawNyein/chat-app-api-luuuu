from rest_framework import serializers
from chat.models import ChatHistory


class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ('sender', 'receiver', 'category', 'message', 'created')
