from django.db import models

# Create your models here.from django.db import models

class Customer(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)  

    def __str__(self):
        return self.username

class Place(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='places/', blank=True, null=True)

    def __str__(self):
        return self.name
    
# Booking Model - Users Book Places
class Booking(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateField()
    guests = models.IntegerField()
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)    

class Itinerary(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)  
    places=models.ManyToManyField(Place) 
    confirmed=models.BooleanField(default=False) 

class AdminProfile(models.Model):
    name=models.CharField(max_length=225,unique=True)
    gmail=models.EmailField(unique=True)
    password=models.CharField(max_length=255)

class Package(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num_people = models.IntegerField()
    destination = models.CharField(max_length=255)
    num_days = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

# class for booking the tour from the index page
class TourBooking(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    date_time = models.DateTimeField()
    destination = models.CharField(max_length=255)
    special_request = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)