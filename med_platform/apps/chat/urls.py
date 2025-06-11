from django.urls import path
from .views import ChatListView, ChatCreateView, DialogsListView

urlpatterns = [
    path('private/<int:receiver_id>/', ChatListView.as_view(), name='chat-list'),
    path('private/<int:receiver_id>/send/', ChatCreateView.as_view(), name='chat-send'),
    path('dialogs/', DialogsListView.as_view(), name='chat-dialogs'),

]
