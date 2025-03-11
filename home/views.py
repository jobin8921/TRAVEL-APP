from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from home.models import Customer
from django.contrib.auth import  logout
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from home.models import Place,Booking,Itinerary
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

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
        username = request.POST['username']
        password = request.POST['password']

        try:
            customer = Customer.objects.get(username=username)
            if check_password(password, customer.password):  # Verify password
                request.session['customer_id'] = customer.id  # Store session
                return redirect('dashboard')  # Redirect to dashboard
            else:
                return HttpResponse("Invalid credentials")
        except Customer.DoesNotExist:
            return HttpResponse("User not found")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)  # Django's inbuilt logout function
    return redirect('index') 

def dashboard(request):
    if 'customer_id' not in request.session:
        return redirect('login')  # Redirect if not logged in
    
    customer = Customer.objects.get(id=request.session['customer_id'])

    places=Place.objects.all()

    return render(request, 'dashboard.html', {'customer': customer,'places':places})

def admin_dashboard(request):
    
    customers = Customer.objects.all()

    places=Place.objects.all()

    return render(request, 'admin_dashboard.html', {'customers': customers,'places':places})

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
    itinerary=Itinerary.objects.get(custormer=request.user)
    itinerary.confirmed=True
    itinerary.save()
    return render(request,'booking_confirmation.html')
