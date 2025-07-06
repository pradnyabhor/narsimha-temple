from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from temple_web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', include([
        path('', views.about, name='about'),
        path('history/', views.history, name='history'),
        path('festivals/', views.festivals, name='festivals'),
        path('pooja/', views.pooja, name='pooja'),
        path('places-to-visit/', views.places_to_visit, name='places_to_visit'),
        path('how-to-reach/', views.how_to_reach, name='how_to_reach'),
    ])),
    path('daily-updates/', views.daily_updates, name='daily_updates'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('events/', views.event_list, name='event_list'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('online-services/', include([
        path('', views.online_services, name='online_services'),
        path('donation/', views.donation, name='donation'),
        path('feedback/', views.feedback, name='feedback'),
        path('sevak-registration/', views.sevak_registration, name='sevak_registration'),
        path('social-activity/', views.social_activity, name='social_activity'),
    ])),
    path('dashboard/', include([
        path('', views.admin_dashboard, name='admin_dashboard'),
        path('sliders/', views.manage_sliders, name='manage_sliders'),
        path('dashboard/sliders/edit/<int:pk>/', views.edit_slider, name='edit_slider'),
        path('dashboard/sliders/delete/<int:pk>/', views.delete_slider, name='delete_slider'),
        path('blogs/', views.manage_blogs, name='manage_blogs'),
        path('events/', views.manage_events, name='manage_events'),
        path('daily-updates/', views.manage_daily_updates, name='manage_daily_updates'),
        path('donations/', views.manage_donations, name='manage_donations'),
        path('feedbacks/', views.manage_feedbacks, name='manage_feedbacks'),
        path('sevaks/', views.manage_sevaks, name='manage_sevaks'),
        path('social-activities/', views.manage_social_activities, name='manage_social_activities'),
        path('about-content/', views.manage_about_content, name='manage_about_content'),
    ])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)

from django.views.static import serve
if settings.DEBUG:
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]