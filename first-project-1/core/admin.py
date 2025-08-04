from django.contrib import admin
from .models import Owner, Dog, Kennel, Booking, DailyLog, Payment, StaffNote, FacilityAvailability

# Custom admin classes to handle missing fields
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'size', 'get_owner_info')
    list_filter = ('size',)
    search_fields = ('name', 'breed')
    readonly_fields = ('id',)
    
    def get_queryset(self, request):
        """Override to avoid accessing photo_base64 field"""
        return Dog.objects.only('id', 'name', 'breed', 'age', 'size', 'owner_id', 'notes')
    
    def get_owner_info(self, obj):
        """Custom method to display owner info without deep JOINs"""
        try:
            return f"Owner {obj.owner_id}"
        except:
            return "Unknown Owner"
    get_owner_info.short_description = 'Owner'

class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('get_booking_info', 'date', 'feeding', 'medication', 'exercise')
    list_filter = ('date',)
    search_fields = ('notes',)
    readonly_fields = ('id',)
    
    def get_queryset(self, request):
        """Override to avoid any JOINs with Dog table"""
        return DailyLog.objects.only('id', 'booking_id', 'date', 'feeding', 'medication', 'exercise', 'notes')
    
    def get_booking_info(self, obj):
        """Custom method to display booking info without JOIN"""
        try:
            return f"Booking {obj.booking_id}"
        except:
            return "Unknown Booking"
    get_booking_info.short_description = 'Booking'

class StaffNoteAdmin(admin.ModelAdmin):
    list_display = ('booking', 'staff_member', 'created_at', 'note')
    list_filter = ('created_at', 'staff_member')
    search_fields = ('note', 'booking__dog__name', 'staff_member__username')
    readonly_fields = ('id', 'created_at')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'status', 'payment_method', 'paid_date')
    list_filter = ('status', 'payment_method', 'paid_date')
    search_fields = ('booking__dog__name', 'notes')
    readonly_fields = ('id', 'created_at')

# Standard Django admin registrations with custom admin classes
admin.site.register(Owner)
admin.site.register(Dog, DogAdmin)
admin.site.register(Kennel)
admin.site.register(Booking)
admin.site.register(DailyLog, DailyLogAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(StaffNote, StaffNoteAdmin)
admin.site.register(FacilityAvailability)
