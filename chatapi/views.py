from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import ChatHistory
from .serializers import ChatHistorySerializer
from rest_framework import mixins, permissions


class ChatHistoryList(ListAPIView):
    queryset = ChatHistory.objects.all()
    serializer_class = ChatHistorySerializer
    pagination_class = PageNumberPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
