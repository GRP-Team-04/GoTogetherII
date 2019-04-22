# Author:Grp group 4
#
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from team_sports_app.models import Profiles

def logout_view(request):
    """ Log out """
    logout(request)
    return HttpResponseRedirect(reverse('team_sports_app:index'))


def register(request):
    """ Register new user"""
    if request.method != 'POST':
        # Show blank register form
        form = UserCreationForm()
    else:
        # process filled forms
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(
                username=new_user.username, password=request.POST['password2'])
            login(request, authenticated_user)

            #add default profile to the user
            new_profile = Profiles()
            new_profile.userID=request.user
            new_profile.name='Need to fill in'
            new_profile.age= 0
            new_profile.speciality='Need to fill in'
            new_profile.email= ''
            new_profile.statement='Need to fill in'
            new_profile.save()
            return HttpResponseRedirect(reverse('team_sports_app:profiles',args=[request.user.username]))

    context = {'form': form}
    return render(request, 'users/register.html', context)
