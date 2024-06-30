from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'company')
    search_fields = list_display
    list_filter = list_display
# Register your models here.
