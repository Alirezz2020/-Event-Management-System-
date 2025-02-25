from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('create/', views.event_create, name='event_create'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/rsvp/', views.submit_rsvp, name='submit_rsvp'),
    path('<int:event_id>/purchase/', views.purchase_ticket, name='purchase_ticket'),
    path('<int:event_id>/feedback/', views.submit_feedback, name='submit_feedback'),
    path('<int:event_id>/analytics/', views.analytics_view, name='analytics'),
]
