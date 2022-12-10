from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(),),
    path('registration/', views.RegistrationAPIView.as_view()),

]
