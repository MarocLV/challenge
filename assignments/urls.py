from django.urls import path
from . import views

urlpatterns = [
    path('hits/', views.list_hits, name='list_hits'),
    path('hitman-assignment/', views.assign_hitman, name='hitman_assignment'),
    path('hits/create/', views.create_hit, name='create_hit'),
]