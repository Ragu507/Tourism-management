from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    # path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('destinations/', DestinationListView.as_view(), name='destinations_list'),
    path('destinations/create/', DestinationCreateView.as_view(), name='destination_create'),
    path('destinations/<int:pk>/', DestinationDetailView.as_view(), name='destination_detail'),
    path('destination/<int:pk>/delete/', DestinationDeleteView.as_view(), name='destination_delete'),

    path('accommodations/', AccommodationListView.as_view(), name='accommodation_list'),
    path('accommodations/<int:pk>/', AccommodationDetailView.as_view(), name='accommodation_detail'),
    path('accommodations/create/', AccommodationCreateView.as_view(), name='accommodation_create'),
    path('accommodations/<int:pk>/edit/', AccommodationUpdateView.as_view(), name='accommodation_update'),
    path('accommodations/<int:pk>/delete/', AccommodationDeleteView.as_view(), name='accommodation_delete'),

    path('tours/', TourListView.as_view(), name='tour_list'),
    path('tours/<int:pk>/', TourDetailView.as_view(), name='tour_detail'),
    path('tours/create/', TourCreateView.as_view(), name='tour_create'),
    path('tours/<int:pk>/update/', TourUpdateView.as_view(), name='tour_update'),
    path('tours/<int:pk>/delete/', TourDeleteView.as_view(), name='tour_delete'),

    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking_create'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/<int:pk>/update/', BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),

    path('reviews/create/', ReviewCreateView.as_view(), name='review_create'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
