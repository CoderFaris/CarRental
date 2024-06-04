from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  Cars, UserInfo, Renting, Rating
from .forms import CustomUserChangeForm, CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserInfo
    list_display = ['username', 'email', 'date_of_birth', 'car_model', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'car_model')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'car_model')}),
    )

admin.site.register(UserInfo, CustomUserAdmin)
admin.site.register(Cars)
admin.site.register(Renting)
admin.site.register(Rating)