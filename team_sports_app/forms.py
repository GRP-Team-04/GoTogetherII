# Author:Grp group 4

from django import forms
from .models import Event, Profiles


class EventForm(forms.ModelForm):
    Event_time = forms.DateTimeField(widget = forms.TextInput(attrs={
                                                                    'id':'datetimepicker1'}))
    class Meta:
        model = Event
        fields = ['Event_name', 'Event_time', 'Event_venue',
                  'Max_players', 'Description']
        labels = {'Event_name': 'Event name', 'Event_time': 'Event time', 'Event_venue': 'Event venue',
                  'Max_players': 'Max players', 'Description': 'Description'}

class ProfilesForm(forms.ModelForm):
	class Meta:
		model = Profiles
		fields = ['name', 'age', 'speciality', 'email', 'statement']
		labels = {'name': 'name', 'age': 'age', 'speciality': 'speciality', 'email': 'email', 'statement': 'statement'}
