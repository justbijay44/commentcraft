
from django.contrib import admin
from django.urls import path
from scraper.views import fetch_comments, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),  # Assuming you want to use fetch_comments for the dashboard
    path('api/fetch-comments/', fetch_comments, name='fetch_comments'),
]
