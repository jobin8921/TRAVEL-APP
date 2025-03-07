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
        return redirect('register')  # Redirect after successful registration

    return render(request, 'registration.html')

