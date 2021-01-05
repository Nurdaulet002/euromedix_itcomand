from django.urls import path
from . import views
app_name = 'patient'
urlpatterns = [
    path('search', views.search, name='search')
]
