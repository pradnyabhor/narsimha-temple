from django.contrib import admin
from .models import *

class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

class AboutContentAdmin(admin.ModelAdmin):
    list_display = ('get_section_display', 'updated_at')
    list_filter = ('section',)

class DailyUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_active')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'content')
    date_hierarchy = 'date'

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}

class DonationAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'is_paid', 'created_at')
    list_filter = ('is_paid',)
    search_fields = ('name', 'email', 'phone')
    date_hierarchy = 'created_at'

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'is_resolved', 'created_at')
    list_filter = ('is_resolved',)
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'created_at'

class SevakRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone', 'skills')
    date_hierarchy = 'created_at'

class SocialActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_active')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'

admin.site.register(Slider, SliderAdmin)
admin.site.register(AboutContent, AboutContentAdmin)
admin.site.register(DailyUpdate, DailyUpdateAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(SevakRegistration, SevakRegistrationAdmin)
admin.site.register(SocialActivity, SocialActivityAdmin)