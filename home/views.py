from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from home.models import Customer
from django.contrib.auth import  logout
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

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

    return render(request, 'dashboard.html', {'customer': customer})

def admin_dashboard(request):
    
    customers = Customer.objects.all()

    return render(request, 'admin_dashboard.html', {'customers': customers})


