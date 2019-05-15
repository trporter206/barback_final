from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Cocktail
# Register your models here.

admin.site.register(Cocktail);

admin.site.register(User, UserAdmin)
