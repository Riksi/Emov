from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [url(r'^$', views.main_page,name='welcome'),
				url(r'^eeg', views.eeg_handler,name='eeg'),
				url(r'^torate',views.retrieve_movies,name='torate'),
				url(r'^ratings',views.receive_ratings,name='ratings')]