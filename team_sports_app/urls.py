""" Define URL patterns for team_sports_app"""

from django.conf.urls import url

from . import views

app_name = 'team_sports_app'
urlpatterns = [
	# Home page
	url(r'^$', views.index, name = 'index'),

	# Show all the events
	url(r'^events/$', views.events, name = 'events'),

	# Show the details of one selected event
	url(r'^events/(?P<user_username>\w+)/(?P<event_id>\d+)/$', views.event, name = 'event'),

	# Add new Event
	url(r'^new_event/$', views.new_event, name='new_event'),

    # Edit existed event

	url(r'^edit_event/(?P<user_username>\w+)/(?P<event_id>\d+)/$', views.edit_event, name="edit_event"),
	url(r'^events/(?P<user_username>\w+)/(?P<event_id>\d+)/join$', views.join, name="join"),
	url(r'^events/(?P<user_username>\w+)/(?P<event_id>\d+)/exit$', views.exit_event, name="exit"),
	url(r'^events/(?P<user_username>\w+)/(?P<event_id>\d+)/delete$', views.delete_event, name="delete"),
	url(r'^profiles/$', views.profiles, name = 'profiles'),

	url(r'^edit_profiles/$', views.edit_profiles, name='edit_profiles'),
	url(r'^save_new_profiles/$', views.save_new_profiles, name='save_new_profiles'),
]
