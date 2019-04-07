from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Event, Participant, Profiles
from django.contrib.auth.models import User
from .forms import EventForm, ProfilesForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    """Home Page of the team sports"""
    return render(request, 'team_sports_app/index.html')


def events(request):
    """Show all of the events"""
    events = Event.objects.order_by('Event_time')
    context = {'events': events, 'what':50}
    return render(request, 'team_sports_app/events.html', context)


@login_required
def event(request, user_username, event_id):
    """Show the details of one selected event"""
    event = Event.objects.get(id=event_id)
    participants = event.participant_set.order_by(('-date_added'))
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
            participant1 = Participant()
            participant1.eventID = new_event;
            participant1.participantID = request.user
            participant1.save()
            return HttpResponseRedirect(reverse('team_sports_app:events'))

    context = {'form': form}
    return render(request, 'team_sports_app/new_event.html', context)


@login_required
def edit_event(request, user_username, event_id):
    """ Edit exist event """

    event = Event.objects.filter(owner=request.user).get(id=event_id)
    #participant = event.participant

    if request.method != 'POST':
        form = EventForm(instance=event)
    else:
        form = EventForm(instance=event, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('team_sports_app:event', args=[user_username, event_id]))
    context = {'event': event, 'form': form}
    return render(request, 'team_sports_app/edit_event.html', context)


def join(request, user_username, event_id):
    """one more parameter 'user_id' or 'pass_in_username' needed here"""

    participant1 = Participant()
    participant1.eventID = Event.objects.get(id=event_id)
    participant1.participantID = User.objects.get(username=user_username)
    if(Participant.objects.filter(participantID=request.user, eventID=event_id).exists()):

        messages.add_message(request, messages.ERROR,
                             "You have already joined this event！")

        return HttpResponseRedirect(reverse('team_sports_app:event', args=[user_username, event_id]))
    else:
        #participant1.date_added = "2019-3-8"
        participant1.save()

        response = "current participant <br>"
        list = Participant.objects.all()
        messages.add_message(request, messages.SUCCESS,
                             "Successfully join the event！")

        """show all rows of table participant, will be changed to HttpResponseRedirect"""
        """for var in list:
			response += var.eventID.Event_name + "  " + var.participantID.username+"<br>"
            return HttpResponse("<p>" + response + "</p>")"""

        return HttpResponseRedirect(reverse('team_sports_app:event', args=[user_username, event_id]))

def profiles(request):
	#return HttpResponse("profiles")

	if(Profiles.objects.filter(userID=request.user).exists()):
		MyProfiles = Profiles.objects.filter(userID=request.user)
		context = {'MyProfiles': MyProfiles}
		return render(request, 'team_sports_app/profiles.html', context)
	else:
		if request.method != 'POST':
        # No data been posted yet: create a new form
			form = ProfilesForm()
		else:
        # POST post datas: process the data
			form = ProfilesForm(request.POST)
			if form.is_valid():
				new_profiles = form.save(commit=False)
				new_profiles.userID = request.user
				new_profiles.save()
				return HttpResponseRedirect(reverse('team_sports_app:profiles'))

		context = {'form': form}
		return render(request, 'team_sports_app/AddProfiles.html', context)

def edit_profiles(request):
	MyProfiles = Profiles.objects.filter(userID=request.user)
	context = {'MyProfiles': MyProfiles}
	return render(request, 'team_sports_app/Edit_Profiles.html', context)

	"""profile = Profiles.objects.get(userID=request.user)
	if request.method != 'POST':
		form = ProfilesForm(instance=profile)
	else:
		form = ProfilesForm(request.POST)
		if form.is_valid():
			form.save()
	context = {'form': form}
	return render(request, 'team_sports_app/AddProfiles.html', context)	"""

def save_new_profiles(request):
	if(request.POST.get('name')==""):
		messages.warning(request, 'The contents of the name cannot be empty')
		return HttpResponseRedirect(reverse('team_sports_app:profiles'))
	else:
		new_profile = Profiles.objects.get(userID=request.user)
		new_profile.userID=request.user
		new_profile.name=request.POST.get('name')
		new_profile.age=request.POST.get('age')
		new_profile.speciality=request.POST.get('speciality')
		new_profile.address=request.POST.get('address')
		new_profile.statement=request.POST.get('statement')
		new_profile.save()
		return HttpResponseRedirect(reverse('team_sports_app:profiles'))

def exit_event(request, user_username, event_id):
    if(Participant.objects.filter(participantID=request.user, eventID=event_id).exists()):
        Participant.objects.get(participantID=request.user, eventID=event_id).delete()
        messages.success(request, 'You are successfully quit from this event!')
    else:
        messages.add_message(request, messages.ERROR,
                             "You haven't in that event yet！")
    return HttpResponseRedirect(reverse('team_sports_app:event', args=[user_username, event_id]))
