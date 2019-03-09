from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Event, Participant
from .forms import EventForm
from django.contrib.auth.decorators import login_required

def index(request):
    """Home Page of the team sports"""
    return render(request, 'team_sports_app/index.html')

def events(request):
    """Show all of the events"""
    events = Event.objects.order_by('Event_time')
    context = {'events': events}
    return render(request, 'team_sports_app/events.html', context)

@login_required
def event(request, event_id):
    """Show the details of one selected event"""
    event = Event.objects.get(id=event_id)
    participants = event.participant_set.order_by('-date_added')
    context = {'event': event, 'participants': participants}

    return render(request, 'team_sports_app/event.html', context)

@login_required
def new_event(request):
    """ Add new event """
    if request.method != 'POST':
        # No data been posted yet: create a new form
        form = EventForm()
    else:
        # POST post datas: process the data
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('team_sports_app:events'))

    context = {'form': form}
    return render(request, 'team_sports_app/new_event.html', context)

@login_required
def edit_event(request, event_id):
    """ Edit exist event """
    
    event = Event.objects.filter(owner=request.user).get(id=event_id)
    #participant = event.participant

    if request.method != 'POST':
        form = EventForm(instance = event)
    else:
        form = EventForm(instance = event, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('team_sports_app:event', args=[event.id]))
    context = {'event': event, 'form': form}
    return render(request, 'team_sports_app/edit_event.html', context)


