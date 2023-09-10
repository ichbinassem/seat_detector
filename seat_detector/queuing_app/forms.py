from django import forms
from .models import QueueEntry

class QueueEntryForm(forms.ModelForm):
    class Meta:
        model = QueueEntry
        fields = ['first_name', 'last_name', 'phone_number', 'email']
