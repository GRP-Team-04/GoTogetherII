from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url

urlpatterns = [
    path('ZvRoo4fuB5bbVsZb3r63/', admin.site.urls),
    path('', include('team_sports_app.urls', namespace = 'team_sports_app')),
    path('users/', include('users.urls', namespace = 'users'))

]
