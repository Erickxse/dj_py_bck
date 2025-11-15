from django.urls import path
from apps.dashboard.views import CexReportView 
from apps.dashboard.views import CexDashboardOverviewView
from apps.dashboard.views.service_product_view import CexServiceProductByStandPaginationView,CexServiceProductCountByStandView,CexServiceProductByIdView,CexServiceProductByUserView 
from apps.dashboard.views.profile_view import ProfileView
from apps.dashboard.views.quote_view import CexQuoteDetailsView,CexQuoteCountByStandView,CexQuoteByStandView,CexQuoteByUserView,CexPaginationQuoteByStandView 

urlpatterns = [
    # Enpoints para Obras
    path('service_product/', CexServiceProductByUserView.as_view(), name='products_by_user'),
    path('service_product/<int:product_id>/', CexServiceProductByIdView.as_view(), name='product_by_id'),
    path('service_product/stand/pagination/', CexServiceProductByStandPaginationView.as_view(), name='products_by_stand_pagination'),
    path('service_product/stand/count/', CexServiceProductCountByStandView.as_view(), name='products_stand_count'),
    # Enpoints para Quotes
    path('quote/', CexQuoteByUserView.as_view(), name='quotes_by_user'),
    path('quote/stand/', CexQuoteByStandView.as_view(), name='quotes_by_stand'),
    path('quote/stand/pagination/', CexPaginationQuoteByStandView.as_view(), name='quotes_by_stand_pagination'),
    path('quote/stand/count/', CexQuoteCountByStandView.as_view(), name='quote_stand_count'),
    path('report/', CexReportView.as_view(), name='quotes_report'),
    path("overview/", CexDashboardOverviewView.as_view(), name="dashboard_overview"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("quote_details/<int:quote_id>/", CexQuoteDetailsView.as_view(), name="quote_details"),

]
