from django import forms
from .models import Event, Profiles


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['Event_name', 'Event_time', 'Event_venue',
                  'Max_players', 'Players_registratered', 'Description']
        labels = {'Event_name': 'Event_name', 'Event_time': 'Event_time', 'Event_venue': 'Event_venue',
                  'Max_players': 'Max_players', 'Players_registratered': 'Players_registratered', 'Description': 'Description'}

class ProfilesForm(forms.ModelForm):
	class Meta:
		model = Profiles
		fields = ['name', 'age', 'speciality', 'address', 'statement']
		labels = {'name': 'name', 'age': 'age', 'speciality': 'speciality', 'address': 'address', 'statement': 'statement'}
		