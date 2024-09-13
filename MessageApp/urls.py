# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:seller_id>/<int:buyer_id>/', views.chat_room, name='chat_room'),
]
