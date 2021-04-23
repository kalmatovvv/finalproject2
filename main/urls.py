from django.urls import path

from main.views import LikeView

urlpatterns = [
    path('like/<int:pk>/', LikeView.as_view()),
]