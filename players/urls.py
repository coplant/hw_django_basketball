from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('teams/', views.team_list, name='team_list'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('matches/', views.match_list, name='match_list'),
    path('matches/past/', views.past_match_list, name='past_match_list')
]
