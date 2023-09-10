
from django.shortcuts import render, redirect
from .forms import QueueEntryForm

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
