from django.urls import path

from .views import get_plans_stands, get_stand_info, get_most_quoted_stands, list_stands, get_active_stands, get_stand_info_by_id, get_all_stands

urlpatterns = [
    # La ruta más específica va primero
    path('api/stand/all/', get_all_stands, name='get_all_stands'),
    path('api/stand/most-quoted/', get_most_quoted_stands, name='most_quoted_stands'),

    # Plans
    path('api/stand/plan/', get_plans_stands, name='get_plans'),
    
    path('api/stand/<path:slug>/', get_stand_info, name='get_stand_info'),
    # La ruta con parámetro va después
    path('api/stand/country/<str:country_code>/', list_stands, name='list_stands'),
    path('api/stand/subscription/plan/', get_active_stands, name='get_active_stands'),
    path('api/stand/id/<int:id>/', get_stand_info_by_id, name='get_stand_info_by_id'), 
    
]