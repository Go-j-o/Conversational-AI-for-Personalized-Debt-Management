from django.urls import path
from .views import chat_view
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path("chat/", chat_view, name="chat"),
]
