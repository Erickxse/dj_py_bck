from django.urls import path
from .views import  list_exhibitions_by_country,exhibition_detail_by_country, exhibitions_details

urlpatterns = [

    path('api/exhibition/<str:country_code>/all/', exhibitions_details, name='exhibition-detail'),
    # Lista las exhibiciones de un país específico identificado por `country_code`.
    # Por ejemplo: /api/exhibition/ec/
    path('api/exhibition/<str:country_code>/', list_exhibitions_by_country, name='list_stands'),
    
    # Muestra los detalles de una exhibición específica de un país identificado por `country_code` y `slug`.
    # Por ejemplo: /api/exhibition/ec/some-exhibition/
    path('api/exhibition/<str:country_code>/<str:slug>/', exhibition_detail_by_country, name='exhibition-detail'),

    path('api/exhibition/<str:country_code>/all/', exhibitions_details, name='exhibition-detail'),
]
