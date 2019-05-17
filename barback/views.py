from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic, View
from django.utils import timezone
from .models import Cocktail, User
from django.db import models
from django.contrib import messages
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from django.template import loader
from django.urls import reverse
import datetime
from .forms import (
    CocktailForm,
    UserForm,
    EditProfileForm,
)
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm
)
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash
)
from django.contrib.auth.models import User

class IndexView(generic.ListView):
    template_name = 'barback/index.html'
    context_object_name = 'latest_cocktails'

    def get_queryset(self):
        return Cocktail.objects.order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Cocktail
    template_name = 'barback/detail.html'

    def get_queryset(self):
        return Cocktail.objects.filter(pub_date__lte=timezone.now())

class CreateView(generic.edit.CreateView):
    model = Cocktail
    fields = ['cocktail_name',
              'cocktail_type',
              'cocktail_image',
              'cocktail_info',
              'cocktail_steps',
              'virgin',
              ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AboutView(generic.TemplateView):
    template_name = "barback/about.html"

class ProfileView(generic.ListView):
    template_name = 'barback/profile.html'
    context_object_name = 'user_cocktails'

    def get_queryset(self):
        return Cocktail.objects.filter(user=self.request.user).order_by('-pub_date')

class RegisterView(generic.edit.CreateView):
    template_name = 'registration/registration_form.html'
    form_class    = UserForm

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

# def register(request):
#     template_name = 'registration/registration_form.html'
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('barback:index')
#     else:
#         form = UserForm()
#         return render(request, template_name, {'form': form})

def save(request, cocktail_id):
    form = CocktailForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(reverse('barback:detail', args=(cocktail.id,)))

def delete(request, cocktail_id):
    model = get_object_or_404(Cocktail, pk=cocktail_id)
    model.delete()
    return HttpResponseRedirect(reverse('barback:index'))

def logout_view(request):
    logout(request)
    return redirect('barback:index')


def edit_profile(request):
    template_name = 'barback/edit_profile.html'
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('barback:profile')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, template_name, {'form': form})

def change_password(request):
    template_name = 'barback/password.html'
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('barback:profile')
        else:
            return redirect('barback:password')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, template_name, {'form': form})
