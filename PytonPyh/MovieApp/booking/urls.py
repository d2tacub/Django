from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),  # Home page for movie selection
    path('ticket/<int:ticket_id>/', views.ticket, name='ticket'),  # Ticket details
]
