from django.urls import path
from . import views, static
from .models import Cocktail
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)

app_name = 'barback'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('cocktail_form/', views.CreateView.as_view(model=Cocktail, success_url=('http://127.0.0.1:8000/barback/')), name='cocktail_form'),
    path('<int:cocktail_id>/save/', views.save, name='save'),
    path('<int:cocktail_id>/delete/', views.delete, name='delete'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html', redirect_field_name=('http://127.0.0.1:8000/barback/')), name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('password/', views.change_password, name='change_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
