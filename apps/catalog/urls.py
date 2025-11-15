from django.urls import path
from .views import get_catalogs_by_stand_and_country, get_catalog_detail

urlpatterns = [
    path('<str:country_code>/<path:stand_slug>/', get_catalogs_by_stand_and_country, name='get_catalogs_by_stand_and_country'),
    path('<str:country_code>/<path:stand_slug>/<path:catalog_slug>/', get_catalog_detail, name='get_catalog_detail'),
]
