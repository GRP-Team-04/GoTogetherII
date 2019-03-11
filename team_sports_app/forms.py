from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['Event_name', 'Event_time', 'Event_venue',
                  'Max_players', 'Players_registratered', 'Description']
        labels = {'Event_name': 'Event_name', 'Event_time': 'Event_time', 'Event_venue': 'Event_venue',
                  'Max_players': 'Max_players', 'Players_registratered': 'Players_registratered', 'Description': 'Description'}
