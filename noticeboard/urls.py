from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', view=views.login, name="index"),
    url(r'^login$', view=views.login, name="login"),
    # url(r'^signup$', view=views.signup, name="signup"),
    url(r'^panel$', view=views.panel, name="panel"),
    url(r'^logout$', view=views.logout, name='logout'),
    url(r'^profile$', view=views.settings, name='profile'),
    url(r'^register$', view=views.registerUser, name='register'),
    url(r'^privacy$', view=views.privacy, name='privacy'),
    url(r'^approve$', view=views.approve, name='approve'),

]
