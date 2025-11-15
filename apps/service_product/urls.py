from django.urls import path
from .views import get_categories_by_stand_slug, get_top_products_by_stand, get_recent_products_by_stand, get_top_products, get_recent_products, get_products_by_stand, get_product_by_slug, get_trending_products, get_products_by_level_3_category,get_products_pagination_by_level_3_category, get_similar_products

urlpatterns = [
    # Rutas generales
    path('api/service_product/<str:country_code>/top_products/', get_top_products, name='get_top_products'),
    path('api/service_product/<str:country_code>/recent_products/', get_recent_products, name='get_recent_products'),  # Nueva ruta
    path('api/service_product/<str:country_code>/trending/', get_trending_products, name='get_trending_products'),
    
    # Rutas específicas
    path('api/service_product/<str:country_code>/<int:category_id>/<slug:stand_slug>/', get_similar_products, name='get_products_by_category_and_stand'),
    path('api/service_product/<str:country_code>/<path:slug>/top_products/', get_top_products_by_stand, name='get_top_products_by_stand'),
    path('api/service_product/<str:country_code>/<path:slug>/recent_products/', get_recent_products_by_stand, name='get_recent_products_by_stand'),
    path('api/service_product/<str:country_code>/<slug:slug>/', get_products_by_stand, name='get_products_by_stand'),
    path('api/service_product/<str:country_code>/<slug:stand_slug>/obra/<slug:product_slug>/', get_product_by_slug, name='get_product_by_slug'),
    path('api/service_product/<str:country_code>/products_category/<slug:category_slug>/', get_products_by_level_3_category, name='get_products_by_level_3_category'),
    path('api/service_product/<str:country_code>/products_category_stand/<slug:slug>/', get_categories_by_stand_slug, name='get_categories_by_stand_slug'),
    
    # Rutas usando paginación
     path('api/service_product/<str:country_code>/products_pag_category/<slug:category_slug>/', get_products_pagination_by_level_3_category, name='get_products_pagination_by_level_3_category'),
]

