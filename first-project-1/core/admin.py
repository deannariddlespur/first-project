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
    list_filter = ('date',)
    search_fields = ('notes',)
    readonly_fields = ('id',)
    
    def get_queryset(self, request):
        """Override to avoid JOIN with Dog table that has missing photo_base64 column"""
        from django.db.models import Prefetch
        return DailyLog.objects.select_related('booking').prefetch_related(
            Prefetch('booking__dog', queryset=Dog.objects.only('id', 'name'))
        )

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
