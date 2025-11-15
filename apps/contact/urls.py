from django.urls import path
from .views import CexInboxCreateView

urlpatterns = [
    path('inbox/', CexInboxCreateView.as_view(), name='cex-inbox-create'),
]
