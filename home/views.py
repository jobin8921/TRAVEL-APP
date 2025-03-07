from django.shortcuts import render



from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from home.models import Customer

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

from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.contrib.auth import login, logout
from home.models import Customer

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
    request.session.flush()  # Clear session
    return redirect('login')

def dashboard(request):
    if 'customer_id' not in request.session:
        return redirect('login')  # Redirect if not logged in
    
    customer = Customer.objects.get(id=request.session['customer_id'])

    return render(request, 'dashboard.html', {'customer': customer})


