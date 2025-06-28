from django.contrib import admin
from .models import Space, UserProfile

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'capacity', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_manager')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('is_manager',)