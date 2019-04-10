# Author:Grp group 4 

from django.db import models
from django.contrib.auth.models import User



class Event(models.Model):
    """Event which users create"""
    Description = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    Event_name = models.CharField(max_length=48)
    Event_time = models.DateTimeField()
    Event_venue = models.CharField(max_length=100)
    Max_players = models.IntegerField()
    Players_registratered = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return string representation(description of event) of model"""
        Players_registratered = 0
        return self.Event_name


class Participant(models.Model):
    """Participants of one Event"""
    eventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    participantID = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'participants'

    def __str__(self):
        return self.eventID.Event_name

class Profiles(models.Model):
	userID = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, null=False)
	age = models.IntegerField(null=True)
	speciality = models.CharField(max_length=100, null=True)
	address = models.CharField(max_length=100, null=True)
	statement = models.CharField(max_length=150, null=True)
