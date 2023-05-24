from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_form),
    path('logout/', views.logout),
    path('register/', views.register),
    path('hitmen/', views.list_hitmen),
    path('hitmen/<str:pk>/', views.hitmen_details),
]