from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('import', views.ImportView),
    path('employee', views.employee),
]
