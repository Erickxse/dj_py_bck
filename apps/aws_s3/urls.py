from django.urls import path
from . import views

urlpatterns = [
    path('api/images/<int:stand_id>/', views.get_image, name='get_image'),
    path('api/images/<int:stand_id>/delete/', views.delete_image, name='delete_image'),
    path('api/dashboard/upload-image/<int:stand_id>/', views.upload_image, name='upload_image'),
    path('api/dashboard/upload-product-image/<int:stand_id>/<int:product_id>/', 
         views.upload_product_image, 
         name='upload_product_image'),
]