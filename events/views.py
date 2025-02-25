from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Event, Ticket, RSVP, Feedback
from .forms import EventForm, RSVPForm, FeedbackForm
from django.db.models import Avg

@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/event_create.html', {'form': form})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    rsvp_form = RSVPForm()
    feedback_form = FeedbackForm()
    context = {
        'event': event,
        'rsvp_form': rsvp_form,
        'feedback_form': feedback_form,
    }
    return render(request, 'events/event_detail.html', context)

@login_required
def submit_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = RSVPForm(request.POST)
        if form.is_valid():
            # Update or create RSVP for the user
            RSVP.objects.update_or_create(
                event=event, user=request.user,
                defaults={'status': form.cleaned_data['status']}
            )
            # Send an email notification for the RSVP
            send_mail(
                subject="RSVP Confirmation",
                message=f"Thank you for your RSVP for {event.title}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True,
            )
            return redirect('events:event_detail', event_id=event.id)
    return redirect('events:event_detail', event_id=event.id)

@login_required
def purchase_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        # Here, you would normally integrate with Stripe/PayPal.
        # For demonstration, we simulate a successful ticket purchase.
        ticket_type = request.POST.get('ticket_type', 'free')
        Ticket.objects.create(event=event, user=request.user, ticket_type=ticket_type)
        # Send a purchase confirmation email
        send_mail(
            subject="Ticket Purchase Confirmation",
            message=f"You have successfully purchased a {ticket_type} ticket for {event.title}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=True,
        )
        return redirect('events:event_detail', event_id=event.id)
    return render(request, 'events/ticket_purchase.html', {'event': event})

@login_required
def submit_feedback(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.event = event
            feedback.user = request.user
            feedback.save()
            return redirect('events:event_detail', event_id=event.id)
    return redirect('events:event_detail', event_id=event.id)

@login_required
def analytics_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    total_tickets = event.tickets.count()
    total_rsvps = event.rsvps.filter(status='attending').count()
    avg_rating = event.feedbacks.aggregate(Avg('rating'))['rating__avg']
    context = {
        'event': event,
        'total_tickets': total_tickets,
        'total_rsvps': total_rsvps,
        'avg_rating': avg_rating,
        'feedbacks': event.feedbacks.all(),
    }
    return render(request, 'events/analytics.html', context)
