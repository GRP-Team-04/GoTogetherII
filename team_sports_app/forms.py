from django import forms
from .models import Event, Profiles


class EventForm(forms.ModelForm):
    Event_time = forms.DateTimeField(widget = forms.TextInput(attrs={
                                                                    'id':'datetimepicker1'}))
    class Meta:
        model = Event
        fields = ['Event_name', 'Event_time', 'Event_venue',
                  'Max_players', 'Players_registratered', 'Description']
        labels = {'Event_name': 'Event name', 'Event_time': 'Event time', 'Event_venue': 'Event venue',
                  'Max_players': 'Max players', 'Players_registratered': 'Players registratered', 'Description': 'Description'}

class ProfilesForm(forms.ModelForm):
	class Meta:
		model = Profiles
		fields = ['name', 'age', 'speciality', 'address', 'statement']
		labels = {'name': 'name', 'age': 'age', 'speciality': 'speciality', 'address': 'address', 'statement': 'statement'}
