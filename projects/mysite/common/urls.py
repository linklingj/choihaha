from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'common'

urlpatterns = [
	path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='common/logout.html'), name='logout'),
	path('signup/', views.signup, name='signup'),
	path('profile/', views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)