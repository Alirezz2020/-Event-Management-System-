from django.contrib import admin
from .models import Venue, Event, Ticket, RSVP, Feedback

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'venue', 'organizer')
    list_filter = ('date', 'venue')
    search_fields = ('title', 'description')

admin.site.register(Ticket)
admin.site.register(RSVP)
admin.site.register(Feedback)
