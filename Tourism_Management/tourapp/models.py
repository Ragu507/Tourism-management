from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='destinations/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Accommodation(models.Model):
    destination = models.ForeignKey(Destination, related_name='accommodations', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=200)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available_rooms = models.PositiveIntegerField()
    image = models.ImageField(upload_to='accommodations/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Tour(models.Model):
    destination = models.ForeignKey(Destination, related_name='tours', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(help_text='Duration of the tour (e.g., 2 hours)')
    image = models.ImageField(upload_to='tours/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey('auth.User', related_name='bookings', on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, null=True, blank=True, on_delete=models.SET_NULL)
    accommodation = models.ForeignKey(Accommodation, null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_people = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - Booking ID: {self.id}'

class Review(models.Model):
    user = models.ForeignKey('auth.User', related_name='reviews', on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, null=True, blank=True, related_name='reviews', on_delete=models.SET_NULL)
    accommodation = models.ForeignKey(Accommodation, null=True, blank=True, related_name='reviews', on_delete=models.SET_NULL)
    destination = models.ForeignKey(Destination, null=True, blank=True, related_name='reviews', on_delete=models.SET_NULL)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - Rating: {self.rating}'


class Activity(models.Model):
    destination = models.ForeignKey(Destination, related_name='activities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(help_text='Duration of the activity')
    image = models.ImageField(upload_to='activities/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

