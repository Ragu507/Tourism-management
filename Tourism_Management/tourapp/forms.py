from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from . models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customizing the username input field
        self.fields['username'].widget.attrs.update({
            'class': 'form-input mt-1 block w-full px-4 py-4 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-gray-900',
            'placeholder': 'Enter your username'
        })
        
        # Customizing the password1 input field
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input mt-1 block w-full px-4 py-4 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-gray-900',
            'placeholder': 'Enter your password'
        })
        
        # Customizing the password2 input field
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input mt-1 block w-full px-4 py-4 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-gray-900',
            'placeholder': 'Confirm your password'
        })


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Enter your password'
        })

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'description', 'location', 'image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['tour', 'accommodation', 'start_date', 'end_date', 'number_of_people']
        widgets = {
            'tour': forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'accommodation': forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'start_date': forms.DateInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'type': 'date'}),
            'number_of_people': forms.NumberInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'total_price': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm bg-gray-100 cursor-not-allowed sm:text-sm', 'readonly': 'readonly'}),
        }
