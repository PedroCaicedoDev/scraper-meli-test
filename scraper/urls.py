# Django
from django.urls import include, path

# Views
from . import views

urlpatterns = [
    path('scraper', views.scraper),
]
