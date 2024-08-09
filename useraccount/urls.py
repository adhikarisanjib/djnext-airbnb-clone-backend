from django.urls import path

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView

from useraccount.api import landlord_detail, reservations_list


urlpatterns = [
    path('login/', LoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('register/', RegisterView.as_view(), name='api_register'),
    path('token/refresh/', get_refresh_view().as_view(), name='api_token_refresh'),
    path('<uuid:id>/', landlord_detail, name='api_landlord_detail'),
    path('reservations/', reservations_list, name='api_reservations_list'),
]
