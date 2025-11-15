from django.urls import path
from .views import CreateQuoteView

urlpatterns = [
    path(
        '<int:stand_id>/product/<int:service_product_id>/quote/',
        CreateQuoteView.as_view(),
        name='create-quote'
    ),
]