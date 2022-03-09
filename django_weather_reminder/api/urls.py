from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django_weather_reminder.api.views.weather_views import (
    CityViewSet, CountryViewSet, UserSubscriptionViewSet
)
from django_weather_reminder.api.views.auth_views import (
    RegistrationAV,
)

registration_view = RegistrationAV.as_view()

country_list = CountryViewSet.as_view({'get': 'list'})
country_detail = CountryViewSet.as_view({'get': 'retrieve'})

city_list = CityViewSet.as_view({'get': 'list'})
city_detail = CityViewSet.as_view({'get': 'retrieve'})

# Subscriptions.
subscription_list = UserSubscriptionViewSet.as_view(
    {'get': 'list', 'post': 'create'}
)
subscription_detail = UserSubscriptionViewSet.as_view(
    {'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}
)


urlpatterns = [
    # JWT auth.
    path('register/', registration_view, name='registration'),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

    # Locations.
    path('countries/', country_list, name='country-list'),
    path('countries/<int:pk>/', country_detail, name='country-detail'),
    path(
        'countries/<int:country_pk>/cities/', city_list, name='city-list'
    ),
    path(
        'countries/<int:country_pk>/cities/<int:pk>/',
        city_detail, name='city-detail'
    ),

    # Subscriptions.
    path(
        'accounts/subscriptions/', subscription_list, name='subscription-list'
    ),
    path(
        'accounts/subscriptions/<int:pk>/', subscription_detail,
        name='subscription-detail'
    )
]
