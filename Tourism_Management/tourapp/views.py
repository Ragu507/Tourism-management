from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Destination, Accommodation, Tour, Booking, Review
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView,LogoutView
from . forms import *

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Save the user and log them in immediately
        user = form.save()
        login(self.request, user)
        return redirect('dashboard') 

class UserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'

class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    ordering = ['-created_at']  

class DestinationCreateView(LoginRequiredMixin, CreateView):
    model = Destination
    form_class = DestinationForm
    template_name = 'destinations/destination_form.html'
    success_url = reverse_lazy('destinations_list')

    def form_valid(self, form):
        # Optionally, you can add extra logic here
        return super().form_valid(form)

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destinations/destination_detail.html'
    context_object_name = 'destination'

class DestinationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Destination
    template_name = 'destinations/destination_confirm_delete.html'
    success_url = reverse_lazy('destination-list')

    def test_func(self):
        # Ensure that only staff or the owner (if applicable) can delete the destination
        return self.request.user.is_staff


class AccommodationListView(ListView):
    model = Accommodation
    template_name = 'accommodations/accommodation_list.html'
    context_object_name = 'accommodations'

    # def get_queryset(self):
    #     destination_id = self.kwargs.get('destination_id')
    #     return Accommodation.objects.filter(destination=destination_id)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['destination'] = get_object_or_404(Destination, id=self.kwargs.get('destination_id'))
    #     return context

class AccommodationDetailView(DetailView):
    model = Accommodation
    template_name = 'accommodations/accommodation_detail.html'
    context_object_name = 'accommodation'

class AccommodationCreateView(LoginRequiredMixin, CreateView):
    model = Accommodation
    fields = ['destination', 'name', 'description', 'address', 'price_per_night', 'available_rooms', 'image']
    template_name = 'accommodations/accommodation_form.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accommodation_detail', kwargs={'pk': self.object.pk})
class AccommodationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Accommodation
    fields = ['name', 'description', 'address', 'price_per_night', 'available_rooms', 'image']
    template_name = 'accommodations/accommodation_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        accommodation = self.get_object()
        return self.request.user == accommodation.owner or self.request.user.is_staff  
class AccommodationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Accommodation
    template_name = 'accommodations/accommodation_confirm_delete.html'
    success_url = reverse_lazy('accommodation-list')

    def test_func(self):
        accommodation = self.get_object()
        return self.request.user == accommodation.owner or self.request.user.is_staff

class TourListView(ListView):
    model = Tour
    template_name = 'tours/tour_list.html'
    context_object_name = 'tours'

    # def get_queryset(self):
    #     return Tour.objects.filter(destination=self.kwargs['destination_id'])


class TourDetailView(DetailView):
    model = Tour
    template_name = 'tours/tour_detail.html'
    context_object_name = 'tour'

class TourCreateView(LoginRequiredMixin, CreateView):
    model = Tour
    fields = ['destination', 'name', 'description', 'price_per_person', 'duration', 'image']
    template_name = 'tours/tour_form.html'

    def get_success_url(self):
        return reverse_lazy('tour_detail', kwargs={'pk': self.object.pk})
    
class TourUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tour
    fields = ['destination', 'name', 'description', 'price_per_person', 'duration', 'image']
    template_name = 'tours/tour_form.html'

    def get_success_url(self):
        return reverse_lazy('tour_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        tour = self.get_object()
        return self.request.user 
    
class TourDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tour
    template_name = 'tours/tour_confirm_delete.html'
    success_url = reverse_lazy('tour_list')

    def test_func(self):
        tour = self.get_object()
        return self.request.user 

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Calculate total price based on the tour or accommodation
        if form.instance.tour:
            form.instance.total_price = form.instance.number_of_people * form.instance.tour.price_per_person
        elif form.instance.accommodation:
            form.instance.total_price = form.instance.number_of_people * form.instance.accommodation.price_per_night
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('booking_detail', kwargs={'pk': self.object.pk})

class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'

    def form_valid(self, form):
        # Calculate total price based on the tour or accommodation
        if form.instance.tour:
            form.instance.total_price = form.instance.number_of_people * form.instance.tour.price_per_person
        elif form.instance.accommodation:
            form.instance.total_price = form.instance.number_of_people * form.instance.accommodation.price_per_night
        return super().form_valid(form)

    def test_func(self):
        booking = self.get_object()
        return self.request.user == booking.user or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('booking_list')

class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('booking-list')

    def test_func(self):
        booking = self.get_object()
        return self.request.user == booking.user

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['tour', 'accommodation', 'destination', 'rating', 'comment']
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Destination, Accommodation, Tour, Booking, Review

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['total_destinations'] = Destination.objects.count()
        context['total_accommodations'] = Accommodation.objects.count()
        context['total_tours'] = Tour.objects.count()
        context['total_bookings'] = Booking.objects.count()
        context['total_reviews'] = Review.objects.count()

        context['recent_bookings'] = Booking.objects.order_by('-created_at')[:5]  # Last 5 bookings
        context['recent_reviews'] = Review.objects.order_by('-created_at')[:5]    # Last 5 reviews
        
        return context
