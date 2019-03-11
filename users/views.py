from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm


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
            return HttpResponseRedirect(reverse('team_sports_app:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)
