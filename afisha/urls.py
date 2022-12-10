"""afisha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from movie_app import views
from . import swagger
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page),
    path('api/v1/static_data/', views.static_data_view),
    # path('api/v1/directors/', views.directors_view),
    path('api/v1/directors/', views.DirectorModelViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/v1/directors/<int:id>/', views.DirectorModelViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('api/v1/movies/', views.movies_view),
    path('api/v1/reviews/', views.reviews_view),
    path('api/v1/movies/reviews/', views.movies_reviews_view),
    path('api/v1/directors/movies/', views.directors_movies_view),
    path('api/v1/movies/<int:id>/', views.movie_item_view),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/genres/', views.GenreListAPIView.as_view()),
    path('api/v1/genres/<int:id>/', views.GenreItemUpdateDeleteAPIView.as_view()),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += swagger.urlpatterns
