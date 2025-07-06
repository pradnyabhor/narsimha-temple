from django import forms
from .models import (
    Donation, Feedback, SevakRegistration,
    Blog, Event, DailyUpdate, SocialActivity,
    Slider, AboutContent
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'email', 'phone', 'amount', 'purpose']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Donate Now'))

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Feedback'))

class SevakRegistrationForm(forms.ModelForm):
    class Meta:
        model = SevakRegistration
        fields = ['name', 'email', 'phone', 'address', 'skills', 'availability']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register as Sevak'))

# Admin Forms
class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['title', 'image', 'description', 'is_active']

class AboutContentForm(forms.ModelForm):
    class Meta:
        model = AboutContent
        fields = ['title', 'content', 'image']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'is_active']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'image', 'start_date', 'end_date', 'location', 'is_active']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class DailyUpdateForm(forms.ModelForm):
    class Meta:
        model = DailyUpdate
        fields = ['title', 'content', 'date', 'is_active']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class SocialActivityForm(forms.ModelForm):
    class Meta:
        model = SocialActivity
        fields = ['title', 'description', 'image', 'date', 'is_active']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }