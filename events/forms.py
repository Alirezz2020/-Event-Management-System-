from django import forms
from .models import Event, RSVP, Feedback
from django.forms.widgets import DateInput, TimeInput

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'venue']
        widgets = {
            'date': forms.TextInput(attrs={
                'class': 'datepicker form-control',
                'placeholder': 'e.g., 2025-03-15'
            }),
            'time': forms.TextInput(attrs={
                'class': 'timepicker form-control',
                'placeholder': 'e.g., 14:30'
            }),
        }
class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['status']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
