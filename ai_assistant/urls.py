from django.urls import path
from . import views

app_name = "ai_assistant"

urlpatterns = [
    path("", views.assistant, name="assistant"),
    path("new/", views.new_conversation, name="new_conversation"),
    path("<int:conversation_id>/", views.conversation, name="conversation"),
    path("<int:conversation_id>/send/", views.send_message, name="send_message"),
    path("conversation/<int:conversation_id>/delete/", views.delete_conversation, name="delete_conversation"),
]