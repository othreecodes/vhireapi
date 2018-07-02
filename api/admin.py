from django.contrib import admin
from . import models
from django.contrib import messages


# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'username', 'email', 'role', 'phone_number']
    list_filter = ['role', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'username']
    actions = ['make_service_provider']

    def make_service_provider(self, request, queryset):
        queryset.update(role="provider")
        messages.info(
            request, f"Created Service ({len(queryset)}) Provider Instance(s)"
        )


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_filter = ['state']
    list_display = ['user', 'state', 'lga', 'address']
    search_fields = ['lga', 'state', 'address']


admin.site.register(models.JobType)
admin.site.register(models.Coupon)
# admin.site.register(models.Service)
admin.site.register(models.ServiceExtra)
admin.site.register(models.Rating)
admin.site.register(models.Session)
admin.site.register(models.JobCategory)

@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['position', 'num_to_apply', 'application_url', 'type']
    list_filter = ['type', 'category']
    search_fields = ['position', 'description']


@admin.register(models.UserIdentification)
class UserIDAdmin(admin.ModelAdmin):
    list_filter = ['verified']


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_filter = ['paid']


@admin.register(models.JobApplication)
class ApplicationAdmin(admin.ModelAdmin):
    list_filter = ['selected']


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['provider', 'customer', 'status', 'price']
    list_filter = ['status']


@admin.register(models.ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['username', 'service', 'booked']
