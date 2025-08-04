from django.contrib import admin
from .models import Owner, Dog, Kennel, Booking, DailyLog, Payment, StaffNote, FacilityAvailability

# Custom admin classes to handle missing fields
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'size', 'owner')
    list_filter = ('size', 'owner')
    search_fields = ('name', 'breed', 'owner__user__username')
    readonly_fields = ('id',)

class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('booking', 'date', 'feeding', 'medication', 'exercise')
    list_filter = ('date', 'booking__dog__name')
    search_fields = ('booking__dog__name', 'notes')
    readonly_fields = ('id',)

# Standard Django admin registrations with custom admin classes
admin.site.register(Owner)
admin.site.register(Dog, DogAdmin)
admin.site.register(Kennel)
admin.site.register(Booking)
admin.site.register(DailyLog, DailyLogAdmin)
admin.site.register(Payment)
admin.site.register(StaffNote)
admin.site.register(FacilityAvailability)
