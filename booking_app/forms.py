from django import forms
from django.utils import timezone
from .models import Booking
from core.models import Space

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'participants', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Динамічне встановлення мінімальної дати
        now = timezone.now().strftime('%Y-%m-%dT%H:%M')
        self.fields['start_time'].widget.attrs['min'] = now
        self.fields['end_time'].widget.attrs['min'] = now