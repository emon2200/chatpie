from django.urls import path
from .views import chatbot_api,widget_view

urlpatterns = [
    path("chat/", chatbot_api, name="chatbot_api"),
      path("chat-widget/<str:api_key>/", widget_view, name="chat_widget")
]
