from django.shortcuts import render
from .models import CexLandingPages
from .serializers import CexLandingPagesSerializer, CexLandingPublicPagesSerializer
from rest_framework import viewsets, permissions

# Create your views here.

class CexLandingPagesView(viewsets.ModelViewSet):
    queryset = CexLandingPages.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CexLandingPagesSerializer


class CexLandingPublicPagesView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = CexLandingPublicPagesSerializer

    def get_queryset(self):
        return CexLandingPages.objects.filter(is_public=1)