from django.contrib import admin
from .models import Mechanic, ServiceRequest

#says how to display search and filter data in admin panel
@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'location', 'rating', 'is_open']
    search_fields = ['name', 'location']

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'mechanic', 'service', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['customer_name', 'vehicle_number']
