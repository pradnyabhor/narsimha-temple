import csv
from urllib.parse import urljoin

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import (
    Slider, AboutContent, DailyUpdate, Blog, Event,
    Donation, Feedback, SevakRegistration, SocialActivity
)
from .forms import (
    DonationForm, FeedbackForm, SevakRegistrationForm,
    SliderForm, AboutContentForm, BlogForm, EventForm,
    DailyUpdateForm, SocialActivityForm
)
import os

# Context processor
def temple_context(request):
    return {
        'temple_name': 'Shri Laxmi Narsinha Mandir',
        'temple_location': 'Ranjani, Maharashtra',
    }


# Frontend Views
def home(request):
    sliders = Slider.objects.filter(is_active=True)
    latest_updates = DailyUpdate.objects.filter(is_active=True).order_by('-date')[:3]
    upcoming_events = Event.objects.filter(is_active=True, start_date__gte=timezone.now()).order_by('start_date')[:3]
    latest_blogs = Blog.objects.filter(is_active=True).order_by('-created_at')[:3]
    social_activities = SocialActivity.objects.filter(is_active=True).order_by('-date')[:3]

    context = {
        'sliders': sliders,
        'latest_updates': latest_updates,
        'upcoming_events': upcoming_events,
        'latest_blogs': latest_blogs,
        'social_activities': social_activities,
    }
    return render(request, 'frontend/home.html', context)


def about(request):
    return render(request, 'frontend/about.html')


def history(request):
    content = get_object_or_404(AboutContent, section='history')
    return render(request, 'frontend/about_section.html', {'content': content, 'section': 'history'})


def festivals(request):
    content = get_object_or_404(AboutContent, section='festivals')
    return render(request, 'frontend/about_section.html', {'content': content, 'section': 'festivals'})


def pooja(request):
    content = get_object_or_404(AboutContent, section='pooja')
    return render(request, 'frontend/about_section.html', {'content': content, 'section': 'pooja'})


def places_to_visit(request):
    content = get_object_or_404(AboutContent, section='places')
    return render(request, 'frontend/about_section.html', {'content': content, 'section': 'places'})


def how_to_reach(request):
    content = get_object_or_404(AboutContent, section='reach')
    return render(request, 'frontend/about_section.html', {'content': content, 'section': 'reach'})


def daily_updates(request):
    updates_list = DailyUpdate.objects.filter(is_active=True).order_by('-date')
    paginator = Paginator(updates_list, 10)
    page_number = request.GET.get('page')
    updates = paginator.get_page(page_number)
    return render(request, 'frontend/daily_updates.html', {'updates': updates})


def blog_list(request):
    blogs_list = Blog.objects.filter(is_active=True).order_by('-created_at')
    paginator = Paginator(blogs_list, 6)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    return render(request, 'frontend/blog_list.html', {'blogs': blogs})


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_active=True)
    recent_blogs = Blog.objects.filter(is_active=True).exclude(id=blog.id).order_by('-created_at')[:3]
    return render(request, 'frontend/blog_detail.html', {'blog': blog, 'recent_blogs': recent_blogs})


def event_list(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(is_active=True, start_date__gte=now).order_by('start_date')
    past_events = Event.objects.filter(is_active=True, end_date__lt=now).order_by('-start_date')
    return render(request, 'frontend/event_list.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'frontend/event_detail.html', {'event': event})


def online_services(request):
    return render(request, 'frontend/online_services.html')


def donation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            # In a real implementation, you would integrate with payment gateway here
            donation.is_paid = True  # Simulating successful payment for demo
            donation.payment_id = f"DEMO-{timezone.now().timestamp()}"
            donation.save()
            messages.success(request, 'Thank you for your donation!')
            return redirect('donation')
    else:
        form = DonationForm()
    return render(request, 'frontend/donation.html', {'form': form})


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback')
    else:
        form = FeedbackForm()
    return render(request, 'frontend/feedback.html', {'form': form})


def sevak_registration(request):
    if request.method == 'POST':
        form = SevakRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for registering as a Sevak! We will contact you soon.')
            return redirect('sevak_registration')
    else:
        form = SevakRegistrationForm()
    return render(request, 'frontend/sevak_registration.html', {'form': form})


def social_activity(request):
    activities = SocialActivity.objects.filter(is_active=True).order_by('-date')
    return render(request, 'frontend/social_activity.html', {'activities': activities})


# Admin Dashboard Views
@login_required
def admin_dashboard(request):
    donation_count = Donation.objects.count()
    feedback_count = Feedback.objects.count()
    sevak_count = SevakRegistration.objects.count()
    event_count = Event.objects.filter(start_date__gte=timezone.now()).count()

    recent_donations = Donation.objects.order_by('-created_at')[:5]
    recent_feedbacks = Feedback.objects.order_by('-created_at')[:5]

    context = {
        'donation_count': donation_count,
        'feedback_count': feedback_count,
        'sevak_count': sevak_count,
        'event_count': event_count,
        'recent_donations': recent_donations,
        'recent_feedbacks': recent_feedbacks,
    }
    return render(request, 'admin/dashboard.html', context)

from django.conf import settings
@login_required
def manage_sliders(request):
    sliders = Slider.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider added successfully!')
            return redirect('manage_sliders')

    else:
        form = SliderForm()
    for slider in sliders:
        slider.image_url = urljoin(settings.MEDIA_URL, slider.image.name)
    return render(request, 'admin/manage_sliders.html', {'form': form, 'sliders': sliders})


@login_required
def edit_slider(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider updated successfully!')
            return redirect('manage_sliders')
    else:
        form = SliderForm(instance=slider)
    return render(request, 'admin/edit_slider.html', {'form': form})


@login_required
def delete_slider(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        slider.delete()
        messages.success(request, 'Slider deleted successfully!')
        return redirect('manage_sliders')
    return render(request, 'admin/delete_slider.html', {'slider': slider})


@login_required
def manage_blogs(request):
    blogs = Blog.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog added successfully!')
            return redirect('manage_blogs')
    else:
        form = BlogForm()
    return render(request, 'admin/manage_blogs.html', {'form': form, 'blogs': blogs})


@login_required
def edit_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog updated successfully!')
            return redirect('manage_blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'admin/edit_blog.html', {'form': form})


@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        # Delete associated image file
        if blog.image:
            if os.path.isfile(blog.image.path):
                os.remove(blog.image.path)
        blog.delete()
        messages.success(request, 'Blog deleted successfully!')
        return redirect('manage_blogs')
    return render(request, 'admin/delete_blog.html', {'blog': blog})


@login_required
def manage_events(request):
    events = Event.objects.all().order_by('-start_date')
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added successfully!')
            return redirect('manage_events')
    else:
        form = EventForm()
    return render(request, 'admin/manage_events.html', {'form': form, 'events': events})


@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('manage_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'admin/edit_event.html', {'form': form})


@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('manage_events')
    return render(request, 'admin/delete_event.html', {'event': event})


@login_required
def manage_daily_updates(request):
    updates = DailyUpdate.objects.all().order_by('-date')
    if request.method == 'POST':
        form = DailyUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Daily update added successfully!')
            return redirect('manage_daily_updates')
    else:
        form = DailyUpdateForm()
    return render(request, 'admin/manage_daily_updates.html', {'form': form, 'updates': updates})


@login_required
def edit_daily_update(request, pk):
    update = get_object_or_404(DailyUpdate, pk=pk)
    if request.method == 'POST':
        form = DailyUpdateForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Daily update updated successfully!')
            return redirect('manage_daily_updates')
    else:
        form = DailyUpdateForm(instance=update)
    return render(request, 'admin/edit_daily_update.html', {'form': form})


@login_required
def delete_daily_update(request, pk):
    update = get_object_or_404(DailyUpdate, pk=pk)
    if request.method == 'POST':
        update.delete()
        messages.success(request, 'Daily update deleted successfully!')
        return redirect('manage_daily_updates')
    return render(request, 'admin/delete_daily_update.html', {'update': update})


@login_required
def manage_donations(request):
    donations_list = Donation.objects.all().order_by('-created_at')
    paginator = Paginator(donations_list, 25)
    page_number = request.GET.get('page')
    donations = paginator.get_page(page_number)

    return render(request, 'admin/manage_donations.html', {'donations': donations})


@login_required
def manage_feedbacks(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        feedbacks = feedbacks.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query)
        )

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter in ['resolved', 'pending']:
        feedbacks = feedbacks.filter(is_resolved=(status_filter == 'resolved'))

    paginator = Paginator(feedbacks, 25)
    page_number = request.GET.get('page')
    feedbacks = paginator.get_page(page_number)

    return render(request, 'admin/manage_feedbacks.html', {
        'feedbacks': feedbacks,
        'search_query': search_query or '',
        'status_filter': status_filter or 'all'
    })

@login_required
def mark_feedback_resolved(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.is_resolved = True
    feedback.save()
    messages.success(request, 'Feedback marked as resolved!')
    return redirect('manage_feedbacks')


@login_required
def manage_sevaks(request):
    sevaks = SevakRegistration.objects.all().order_by('-created_at')
    return render(request, 'admin/manage_sevaks.html', {'sevaks': sevaks})


@login_required
def manage_social_activities(request):
    activities = SocialActivity.objects.all().order_by('-date')
    if request.method == 'POST':
        form = SocialActivityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Social activity added successfully!')
            return redirect('manage_social_activities')
    else:
        form = SocialActivityForm()
    return render(request, 'admin/manage_social_activities.html', {'form': form, 'activities': activities})


@login_required
def edit_social_activity(request, pk):
    activity = get_object_or_404(SocialActivity, pk=pk)
    if request.method == 'POST':
        form = SocialActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Social activity updated successfully!')
            return redirect('manage_social_activities')
    else:
        form = SocialActivityForm(instance=activity)
    return render(request, 'admin/edit_social_activity.html', {'form': form})


@login_required
def delete_social_activity(request, pk):
    activity = get_object_or_404(SocialActivity, pk=pk)
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Social activity deleted successfully!')
        return redirect('manage_social_activities')
    return render(request, 'admin/delete_social_activity.html', {'activity': activity})


@login_required
def manage_about_content(request):
    sections = AboutContent.objects.all()
    section_id = request.GET.get('section')

    if section_id:
        section = get_object_or_404(AboutContent, pk=section_id)
    else:
        section = sections.first() if sections else None

    if request.method == 'POST':
        form = AboutContentForm(request.POST, request.FILES, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, 'Content updated successfully!')
            return redirect('manage_about_content')
    else:
        form = AboutContentForm(instance=section)

    return render(request, 'admin/manage_about_content.html', {
        'sections': sections,
        'form': form,
        'current_section': section,
    })


@login_required
def manage_donations(request):
    donations = Donation.objects.all().order_by('-created_at')

    # Export to CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="donations.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone', 'Amount', 'Purpose', 'Date', 'Status'])

        for donation in donations:
            writer.writerow([
                donation.name,
                donation.email,
                donation.phone,
                donation.amount,
                donation.purpose or '',
                donation.created_at.strftime('%Y-%m-%d'),
                'Paid' if donation.is_paid else 'Pending'
            ])

        return response

    # Regular paginated view
    paginator = Paginator(donations, 25)
    page_number = request.GET.get('page')
    donations = paginator.get_page(page_number)

    return render(request, 'admin/manage_donations.html', {'donations': donations})