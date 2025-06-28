from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('space', 'user', 'start_time', 'end_time', 'status', 'participants')
    list_filter = ('status', 'space__type')
    search_fields = ('user__user__username', 'space__name', 'notes')
    date_hierarchy = 'start_time'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('user', 'space')}),
        ('Час', {'fields': ('start_time', 'end_time')}),
        ('Деталі', {'fields': ('status', 'participants', 'notes')}),
        ('Метадані', {'fields': ('created_at', 'updated_at')}),
    )