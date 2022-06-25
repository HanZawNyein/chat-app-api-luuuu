from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from chatapi.views import ChatHistoryList

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('chat-history/<int:sender>/<int:receiver>/', ChatHistoryList.as_view(), name="chat_history")
]
