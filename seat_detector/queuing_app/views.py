
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import QueueEntryForm, SignupForm, SigninForm
from .models import Restaurant
from .forms import RestaurantCodeForm


def main_page(request):
    if request.method == 'POST':
        form = QueueEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = QueueEntryForm()

    return render(request, 'main.html', {'form': form})

def success_page(request):
    return render(request, 'success.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashed_password = make_password(password)
            User.objects.create(username=email, email=email, password=hashed_password)
            # Handle the data, e.g., save to the database
            # For passwords, make sure to hash before saving!
            return redirect('success')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # If the user exists and the password is correct, log them in
                login(request, user)
                return redirect('success')
            else:
                # If the credentials are incorrect, show an error message
                messages.error(request, 'Invalid email or password')
    else:
        form = SigninForm()
    return render(request, 'signin.html', {'form': form})

def enter_code_view(request):
    if request.method == 'POST':
        entered_code = request.POST.get('restaurant_code')
        
        # Check if the entered code matches any restaurant in the database
        matching_restaurant = Restaurant.objects.filter(code=entered_code).first()
        
        if matching_restaurant:
            # If there's a match, do something (e.g., redirect to another page)
            return redirect('success')
        else:
            # If no match, return an error or handle accordingly
            context = {'error_message': 'Invalid restaurant code'}
            return render(request, 'main.html', context)

    return render(request, 'main.html')