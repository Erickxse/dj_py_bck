from rest_framework import routers
from django.urls import path, include
from .views import CategoryView, CategoryTreeView, CategoryCarouselView, CategorySubView 

router = routers.DefaultRouter()

router.register('category', CategoryView, 'category')

router.register('api/category_carousel/(?P<slug>[^/.]+)', CategoryCarouselView, basename='category_carousel')

urlpatterns = [
    path('api/category/', include(router.urls)),
    path('api/category/category_tree/', CategoryTreeView.as_view({'get': 'list'}), name='category_tree'),
    path('api/category/category_carousel/', CategoryCarouselView.as_view({'get': 'list'}), name='category_carousel'),
    path('api/category/category_sub/<slug:slug>/', CategorySubView.as_view({'get': 'list'}), name='category_sub_slug'),
]
