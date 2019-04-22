# Author:Grp group 4

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
    context = {'events': events}
    return render(request, 'team_sports_app/events.html', context)

@login_required
def my_event(request):
    # show current user's event
    my = request.user
    myownevents = my.event_set.order_by(('date_added'))
    # myjoinedevent = Pa
    context = {'myownevents': myownevents}
    return render(request, 'team_sports_app/myevents.html', context)

@login_required
def event(request, event_id):
    """Show the details of one selected event"""
    try:
        event = Event.objects.get(id=event_id)
    except Exception as e:
        return HttpResponseRedirect(reverse('team_sports_app:events'))

    participants = event.participant_set.order_by(('-date_added'))
    isOwner = (event.owner == request.user)
    isJoined = Participant.objects.filter(participantID=request.user, eventID=event_id).exists()
    context = {'event': event, 'participants': participants,'isJoined' : isJoined, 'isOwner' : isOwner}

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
def edit_event(request, event_id):
    """ Edit exist event """

    event = Event.objects.filter(owner=request.user).get(id=event_id)
    #participant = event.participant

    if request.method != 'POST':
        form = EventForm(instance=event)
    else:
        form = EventForm(instance=event, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('team_sports_app:event', args=[event_id]))
    context = {'event': event, 'form': form}
    return render(request, 'team_sports_app/edit_event.html', context)


def join(request, event_id):
    """one more parameter 'user_id' or 'pass_in_username' needed here"""

    participant1 = Participant()
    try:
        event = Event.objects.get(id=event_id)
    except Exception as e:
        messages.error(request, 'The Event is not exist anymore!')
        return HttpResponseRedirect(reverse('team_sports_app:events'))

    if (event.Max_players == event.Players_registratered):
        messages.error(request, 'The team is full, please browser other events!')
    elif(Participant.objects.filter(participantID=request.user, eventID=event_id).exists()):
        messages.add_message(request, messages.ERROR,
                             "You have already joined this event！")

        return HttpResponseRedirect(reverse('team_sports_app:event', args=[event_id]))
    else:
        participant1.eventID = event
        participant1.participantID = User.objects.get(username=request.user)
        participant1.save()
        event.Players_registratered += 1
        event.save();

        messages.add_message(request, messages.SUCCESS,
                             "Successfully join the event！")

        return HttpResponseRedirect(reverse('team_sports_app:event', args=[event_id]))

def profiles(request, whoseprofile):
	#return HttpResponse("profiles")
	Who = User.objects.get(username=whoseprofile)
	if(Profiles.objects.filter(userID=Who).exists()):
		MyProfiles = Profiles.objects.filter(userID=Who)
		isOwner = (request.user == Who)
		context = {'MyProfiles': MyProfiles,'isOwner':isOwner}
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
				return HttpResponseRedirect(reverse('team_sports_app:profiles',args=[whoseprofile]))

		context = {'form': form, 'isOwner':True}
		return render(request, 'team_sports_app/AddProfiles.html', context)

def edit_profiles(request):
	MyProfiles = Profiles.objects.filter(userID=request.user)
	context = {'MyProfiles': MyProfiles}
	return render(request, 'team_sports_app/Edit_Profiles.html', context)

def save_new_profiles(request):
	if(request.POST.get('name')==""):
		messages.warning(request, 'The contents of the name cannot be empty')
		return HttpResponseRedirect(reverse('team_sports_app:profiles',args=[request.user]))
	else:
		new_profile = Profiles.objects.get(userID=request.user)
		new_profile.userID=request.user
		new_profile.name=request.POST.get('name')
		new_profile.age=request.POST.get('age')
		new_profile.speciality=request.POST.get('speciality')
		new_profile.address=request.POST.get('address')
		new_profile.statement=request.POST.get('statement')
		new_profile.save()
		return HttpResponseRedirect(reverse('team_sports_app:profiles',args=[request.user]))

def exit_event(request,event_id):

    if(Participant.objects.filter(participantID=request.user, eventID=event_id).exists()):
        try:
            event = Event.objects.get(id = event_id)
            Participant.objects.get(participantID=request.user, eventID=event_id).delete()
            event.Players_registratered -= 1
            event.save()
        except Exception as e:
            messages.error(request, 'The Event is not exist anymore!')
            return HttpResponseRedirect(reverse('team_sports_app:events'))
        messages.success(request, 'You are successfully quit from this event!')
    else:
        messages.add_message(request, messages.ERROR,
                             "You haven't in that event yet！")
    return HttpResponseRedirect(reverse('team_sports_app:event', args=[event_id]))

def delete_event(request,event_id):
        Event.objects.get(id=event_id).delete()
        messages.success(request, 'You are successfully delete this event!')

        return HttpResponseRedirect(reverse('team_sports_app:events'))
