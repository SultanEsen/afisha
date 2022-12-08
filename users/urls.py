from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.login,),
    path('registration/', views.registration),

]
