from .models import (
    Slider, AboutContent, DailyUpdate, Blog, Event,
    Donation, Feedback, SevakRegistration, SocialActivity
)
from django.utils import timezone

def temple_context(request):
    return {
        'temple_name': 'Shri Laxmi Narsinha Mandir',
        'temple_location': 'Ranjani, Maharashtra',
        'current_year': timezone.now().year,
    }