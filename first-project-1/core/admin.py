from django.contrib import admin
from .models import Owner, Dog, Kennel, Booking, DailyLog, Payment, StaffNote, FacilityAvailability

# Custom admin classes
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'size', 'get_owner_info')
    list_filter = ('size',)
    search_fields = ('name', 'breed')
    readonly_fields = ('id',)
    
    def get_queryset(self, request):
        """Optimized queryset for admin display"""
        return Dog.objects.only('id', 'name', 'breed', 'age', 'size', 'owner_id', 'notes')
    
    def get_owner_info(self, obj):
        """Custom method to display owner info"""
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
        """Optimized queryset for admin display"""
        return DailyLog.objects.only('id', 'booking_id', 'date', 'feeding', 'medication', 'exercise', 'notes')
    
    def get_booking_info(self, obj):
        """Custom method to display booking info"""
        try:
            return f"Booking {obj.booking_id}"
        except:
            return "Unknown Booking"
    get_booking_info.short_description = 'Booking'

class StaffNoteAdmin(admin.ModelAdmin):
    list_display = ('get_booking_info', 'get_staff_info', 'created_at', 'note')
    list_filter = ('created_at',)
    search_fields = ('note',)
    readonly_fields = ('id', 'created_at')
    
    def get_queryset(self, request):
        """Optimized queryset for admin display"""
        return StaffNote.objects.only('id', 'booking_id', 'staff_member_id', 'note', 'picture', 'created_at')
    
    def get_booking_info(self, obj):
        """Custom method to display booking info"""
        try:
            return f"Booking {obj.booking_id}"
        except:
            return "Unknown Booking"
    get_booking_info.short_description = 'Booking'
    
    def get_staff_info(self, obj):
        """Custom method to display staff info"""
        try:
            return f"Staff {obj.staff_member_id}"
        except:
            return "Unknown Staff"
    get_staff_info.short_description = 'Staff Member'

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('get_booking_info', 'amount', 'status', 'payment_method', 'paid_date')
    list_filter = ('status', 'payment_method', 'paid_date')
    search_fields = ('notes',)
    readonly_fields = ('id', 'created_at')
    
    def get_queryset(self, request):
        """Optimized queryset for admin display"""
        return Payment.objects.only('id', 'booking_id', 'amount', 'status', 'payment_method', 'paid_date', 'notes', 'created_at')
    
    def get_booking_info(self, obj):
        """Custom method to display booking info"""
        try:
            return f"Booking {obj.booking_id}"
        except:
            return "Unknown Booking"
    get_booking_info.short_description = 'Booking'

# Standard Django admin registrations with custom admin classes
admin.site.register(Owner)
admin.site.register(Dog, DogAdmin)
admin.site.register(Kennel)
admin.site.register(Booking)
admin.site.register(DailyLog, DailyLogAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(StaffNote, StaffNoteAdmin)
admin.site.register(FacilityAvailability)
