from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'authentication'
urlpatterns = [
	path('', auth_views.LoginView.as_view(
		template_name='authentication/login.html'), name='login'),
	path('identify/role',views.identifyRole, name='identifyRole'),
]