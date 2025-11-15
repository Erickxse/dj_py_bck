from rest_framework import routers
from django.urls import path, include
from .views import CexLandingPagesView, CexLandingPublicPagesView

router = routers.DefaultRouter()

router.register('market', CexLandingPagesView, 'market')
router.register('public_market', CexLandingPublicPagesView, 'public_market')

urlpatterns = [
    path('api/market/', include(router.urls)),
]
