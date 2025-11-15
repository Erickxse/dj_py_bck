from django.urls import path
from .views import SearchPaginationView, SearchResultsView

urlpatterns = [
    path('api/search/', SearchPaginationView.as_view(), name='search'),
    path('api/search/results/', SearchResultsView.as_view(), name='search-results'),
]
