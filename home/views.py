from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from home.models import Customer,AdminProfile
from django.contrib.auth import  logout
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from home.models import Place,Booking,Itinerary
from django.contrib import messages
import razorpay
from django.conf import settings
from django.http import JsonResponse



def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request,'service.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        gender = request.POST['gender']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']

        # Save user
        customer = Customer(
            username=username,
            email=email,
            phone_number=phone_number,
            password=make_password(password),  # Hashing password
            gender=gender,
            city=city,
            state=state,
            country=country
        )
        customer.save()
        return redirect('login')  # Redirect after successful registration

    return render(request, 'registration.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if user is an admin
        try:
            admin = AdminProfile.objects.get(name=username, password=password)
            request.session["admin_id"] = admin.id  # Store admin session
            return redirect("admin_dashboard")  # Redirect to admin panel if admin
        except AdminProfile.DoesNotExist:
            pass  # Continue checking regular users

        # Check if user is a regular customer
        try:
            user = Customer.objects.get(username=username)
            if check_password(password, user.password):  # Securely check hashed password
                request.session["customer_id"] = user.id
                return redirect("dashboard")  # Redirect normal user to dashboard
        except Customer.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid credentials."})

    return render(request, "login.html")

def logout_view(request):
    logout(request)  # Django's inbuilt logout function
    return redirect('index') 

def dashboard(request):
    if 'customer_id' not in request.session:
        return redirect('login')  # Redirect if not logged in
    
    customer = Customer.objects.get(id=request.session['customer_id'])

    places=Place.objects.all()

    return render(request, 'dashboard.html', {'customer': customer,'places':places})


# Import models

def admin_dashboard(request):
    if "admin_id" not in request.session:
        return redirect("login")  # Redirect if not logged in as admin
    
    # Get the current logged-in admin
    try:
        admin_user = AdminProfile.objects.get(id=request.session["admin_id"])
    except AdminProfile.DoesNotExist:
        return redirect("login")  # Redirect if session ID is invalid
    
    customers = Customer.objects.filter(is_admin=False)

    confirmed_bookings = Itinerary.objects.filter(confirmed=True)
    places = Place.objects.all()
    admins = AdminProfile.objects.all()  # Get all admins

    return render(request, "admin_dashboard.html", {
        "admin_user": admin_user,
        "admins": admins,
        "confirmed_bookings": confirmed_bookings,
        "places": places,
        'customers':customers,
    })



def add_place(request):

    if request.method=='POST':

        name=request.POST.get('name')
        location=request.POST.get('location')
        description=request.POST.get('description')
        image=request.FILES.get('image')

        if name and location and description:
            place=Place(name=name,location=location,description=description)

            if image:

              place.image=image

        place.save()
        return redirect('admin_dashboard')    
    
    return render(request,'add_place.html')


def book_place(request):
    places = Place.objects.all()  # Fetch all places for the dropdown
    if request.method=='POST':
        place_id=request.POST.get('place_id')
        date=request.POST.get('date')
        guests=request.POST.get('guests')
        special_request=request.POST.get('requests')

        place=get_object_or_404(Place,id=place_id)
        booking=Booking.objects.create(user=request.user,place=place,date=date,guests=guests,special_request=special_request)
        messages.success(request,"Your booking has been confirmed")
        
        return redirect("dashboard")
    
    return render(request,'booking.html',{'places':places})



def add_to_itinerary(request, place_id):
    if 'customer_id' not in request.session:
        return redirect('login')  # Redirect if not logged in

    # Fetch the customer using session data
    customer_id = request.session['customer_id']
    customer = get_object_or_404(Customer, id=customer_id)

    place = get_object_or_404(Place, id=place_id)
    
    # Get or create itinerary for this customer
    itinerary, created = Itinerary.objects.get_or_create(customer=customer)

    # Add the selected place to the itinerary
    itinerary.places.add(place)

    return redirect('view_itinerary')


def view_itinerary(request):
    if 'customer_id' not in request.session:
        return redirect('login')  # Redirect if not logged in

    # Fetch the customer from session
    customer_id = request.session['customer_id']
    customer = get_object_or_404(Customer, id=customer_id)

    # Get the itinerary for the logged-in customer
    itinerary, created = Itinerary.objects.get_or_create(customer=customer)

    return render(request, 'view_itinerary.html', {'itinerary': itinerary})


def confirm_booking(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer_id = request.session['customer_id']
    customer = get_object_or_404(Customer, id=customer_id)

    itinerary = get_object_or_404(Itinerary, customer=customer)

    # Set the booking amount (Assume each booking costs ₹1000)
    amount = 1000 * 100  # Amount in paise (₹1000 = 100000 paise)

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create a Razorpay Order
    order_data = {
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"  # Auto-capture payment
    }
    order = client.order.create(order_data)

    # Save the order ID in session (to verify later)
    request.session['razorpay_order_id'] = order['id']

    return render(request, 'payment.html', {
        "customer": customer,
        "itinerary": itinerary,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "order_id": order['id']
    })



def payment_success(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer_id = request.session['customer_id']
    customer = get_object_or_404(Customer, id=customer_id)

    itinerary = get_object_or_404(Itinerary, customer=customer)
    
    # Mark itinerary as confirmed
    itinerary.confirmed = True
    itinerary.save()

    return render(request, 'payment_success.html', {"customer": customer, "itinerary": itinerary})



def register_admin(request):
    if request.method == "POST":
        name = request.POST.get("name")
        gmail = request.POST.get("gmail")
        password = request.POST.get("password")

        # Ensure fields are not empty
        if name and gmail and password:
            if not AdminProfile.objects.filter(name=name).exists():
                AdminProfile.objects.create(name=name, gmail=gmail, password=password)
                return redirect("login")  # Redirect to login after successful registration
            else:
                return render(request, "admin_register.html", {"error": "Admin username already exists."})

    return render(request, "admin_register.html")
