from django.urls import path
from apps.superadmin.views.create_stand_view import CreateStandView
from apps.superadmin.views.plan_view import PlanView
from apps.superadmin.views.subscription_view import SubscriptionView
from apps.superadmin.views.stand_view import AllStandsView
from apps.superadmin.views.user_stand_list_view import UserStandListView
from apps.superadmin.views.stand_view import StandDetailView
from apps.superadmin.views.create_stand_view import UpdateStandView

urlpatterns = [
    path('subscription/<int:stand_id>/',
         SubscriptionView.as_view(), name='get_subscription_info'),
    path('stands/', 
         AllStandsView.as_view(), 
         name='get_all_stands'),
    path('stands/<int:id>/', StandDetailView.as_view(), name='stand_detail'),
    path('stands/update/<int:id>/', UpdateStandView.as_view(), name='update_stand'),
    path('plans/', PlanView.as_view(), name='get_all_plans'),
    path('new_stand/', CreateStandView.as_view(),  name='create_stand'),
    path('user_stand_list/', UserStandListView.as_view(), name='user_stand_list'),

]
