from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Event, Participant
from django.contrib.auth.models import User
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    """Home Page of the team sports"""
    return render(request, 'team_sports_app/index.html')

def events(request):
    """Show all of the events"""
    events = Event.objects.order_by('Event_time')
    context = {'events': events}
    return render(request, 'team_sports_app/events.html', context)

@login_required
def event(request, user_username, event_id):
    """Show the details of one selected event"""
    event = Event.objects.get(id=event_id)
    participants = event.participant_set.order_by('date_added')
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
            new_event = form.save(commit=False)
            new_event.owner = request.user
            new_event.save()
            return HttpResponseRedirect(reverse('team_sports_app:events'))

    context = {'form': form}
    return render(request, 'team_sports_app/new_event.html', context)

@login_required
def edit_event(request, user_username, event_id):
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

def join(request, user_username, event_id):
	"""one more parameter 'user_id' or 'pass_in_username' needed here"""

	participant1 = Participant()
	participant1.eventID = Event.objects.get(id=event_id)
	participant1.participantID = User.objects.get(username=user_username)
	if(Participant.objects.filter(participantID=request.user,eventID=event_id).exists()):

		messages.add_message(request, messages.ERROR, "You have already joined this event！")

		return HttpResponseRedirect(reverse('team_sports_app:event', args=[user_username,event_id]))
	else:
		#participant1.date_added = "2019-3-8"
		participant1.save()

		response = "current participant <br>"
		list = Participant.objects.all()

		"""show all rows of table participant, will be changed to HttpResponseRedirect"""
		"""for var in list:
			response += var.eventID.Event_name + "  " + var.participantID.username+"<br>"

		return HttpResponse("<p>" + response + "</p>")"""
		return HttpResponseRedirect(reverse('team_sports_app:event', args=[user_username,event_id]))
