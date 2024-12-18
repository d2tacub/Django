from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin panel
    path('', include('booking.urls')),  # Routes for the booking app
]
