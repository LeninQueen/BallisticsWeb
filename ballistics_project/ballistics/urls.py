from django.urls import path
from . import views

app_name = 'ballistics'

urlpatterns = [
    path('', views.ballistics_view, name='calculate'),
]