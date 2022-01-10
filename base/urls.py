from django.urls import path
from .           import views


urlpatterns = [
    path('',                      views.index,              name='home'),
    path('login/',                views.user_login,         name='login'),
    path('logout/',               views.user_logout,        name='logout'),
    path('media/<str:file_type>/<str:file>', views.MediaSecurityCheck, name='media'),

]
