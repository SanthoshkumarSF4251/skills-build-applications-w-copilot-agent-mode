"""octofit_tracker URL Configuration

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
from rest_framework.routers import DefaultRouter

import os
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from . import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'activities', views.ActivityViewSet, basename='activity')
router.register(r'workouts', views.WorkoutViewSet, basename='workout')
router.register(r'leaderboard', views.LeaderboardViewSet, basename='leaderboard')

CODESPACE_NAME = os.environ.get('CODESPACE_NAME')
def get_api_url(request, path):
    if CODESPACE_NAME:
        base = f'https://{CODESPACE_NAME}-8000.app.github.dev'
    else:
        base = request.build_absolute_uri('/')[:-1]
    return f'{base}/api/{path}'

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': get_api_url(request, 'users/'),
        'teams': get_api_url(request, 'teams/'),
        'activities': get_api_url(request, 'activities/'),
        'workouts': get_api_url(request, 'workouts/'),
        'leaderboard': get_api_url(request, 'leaderboard/'),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', views.api_root, name='api-root'),
]
