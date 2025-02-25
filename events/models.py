from django.db import models
from django.contrib.auth.models import User


class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    purchase_date = models.DateTimeField(auto_now_add=True)
    ticket_type = models.CharField(max_length=50, choices=[('free', 'Free'), ('paid', 'Paid')])

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.ticket_type})"


class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rsvps')
    status = models.CharField(max_length=20, choices=[('attending', 'Attending'), ('not_attending', 'Not Attending')])
    responded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} RSVP for {self.event.title}"


class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveIntegerField()  # For a rating scale (e.g., 1-5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} for {self.event.title}"
