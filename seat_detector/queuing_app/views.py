
from django.shortcuts import render, redirect
from .forms import QueueEntryForm, SignupForm

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
            # Handle the data, e.g., save to the database
            # For passwords, make sure to hash before saving!
            return redirect('success_page')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
