from django.urls import path
from tourists.views import TouristProfileView, TouristProfileDetailView, CurrentUserProfileView

urlpatterns = [
    path('tourists/', TouristProfileView.as_view(),),
    path('current-user/', CurrentUserProfileView.as_view(), ),
    path('tourists/<int:pk>/', TouristProfileDetailView.as_view(),),
]
