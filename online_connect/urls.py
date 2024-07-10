from django.urls import path

from online_connect.views import *


urlpatterns = [
    path('list_of_doctors',list_of_doctors,name="list_of_doctors"),
    path('book_appointment/<int:id>',book_appointment,name="book_appointment") ,
    path('appointments',appointments,name="appointments"),
    path('init_event/<int:id>',create_appointment_event,name="init_event"),
    path('callback',google_calendar_redirect_view,name="callback")
]