from django.contrib import admin
from .models import Owner, Dog, Kennel, Booking, DailyLog, Payment, StaffNote, FacilityAvailability

# Standard Django admin registrations - no custom styling
# Note: User model is already registered by Django's auth admin
admin.site.register(Owner)
admin.site.register(Dog)
admin.site.register(Kennel)
admin.site.register(Booking)
admin.site.register(DailyLog)
admin.site.register(Payment)
admin.site.register(StaffNote)
admin.site.register(FacilityAvailability)
