from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('quiz/<int:task_id>/', views.quiz_view, name='quiz'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('profile/', views.profile_view, name='profile'),
]
