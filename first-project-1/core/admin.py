from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Owner, Dog, Kennel, Booking, DailyLog, Payment, StaffNote, FacilityAvailability

# Custom Admin Site
class DogBoardingAdminSite(AdminSite):
    site_header = "🐕 Dog Boarding Admin"
    site_title = "Dog Boarding Management"
    index_title = "Welcome to Dog Boarding Administration"
    site_url = "/"

# Create custom admin site instance
dogboarding_admin = DogBoardingAdminSite(name='dogboarding_admin')

# Custom Admin Classes
class BookingAdmin(admin.ModelAdmin):
    list_display = ['dog', 'owner', 'start_date', 'end_date', 'status', 'kennel', 'total_amount']
    list_filter = ['status', 'start_date', 'kennel__size']
    search_fields = ['dog__name', 'dog__owner__user__username', 'notes']
    date_hierarchy = 'start_date'
    readonly_fields = ['total_amount', 'price_per_night']
    
    def owner(self, obj):
        return obj.dog.owner if obj.dog else "N/A"
    owner.short_description = "Owner"

class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'age', 'size', 'owner', 'photo_display']
    list_filter = ['size', 'breed']
    search_fields = ['name', 'breed', 'owner__user__username']
    
    def photo_display(self, obj):
        if obj.photo:
            return f"📸 Photo uploaded"
        return "No photo"
    photo_display.short_description = "Photo"

class KennelAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'description', 'availability_status']
    list_filter = ['size']
    search_fields = ['name', 'description']
    
    def availability_status(self, obj):
        return "✅ Available" if obj.is_available_for_dates() else "❌ Occupied"
    availability_status.short_description = "Status"

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['booking__dog__name', 'booking__dog__owner__user__username']
    date_hierarchy = 'created_at'

class StaffNoteAdmin(admin.ModelAdmin):
    list_display = ['booking', 'staff_member', 'note_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['note', 'booking__dog__name']
    date_hierarchy = 'created_at'
    
    def note_preview(self, obj):
        return obj.note[:50] + "..." if len(obj.note) > 50 else obj.note
    note_preview.short_description = "Note"

class FacilityAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['date', 'type', 'title', 'description']
    list_filter = ['type', 'date']
    search_fields = ['title', 'description']
    date_hierarchy = 'date'

class OwnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', 'dog_count']
    search_fields = ['user__username', 'user__email', 'phone']
    
    def dog_count(self, obj):
        return obj.dogs.count()
    dog_count.short_description = "Dogs"

# Register models with custom admin site
dogboarding_admin.register(Owner, OwnerAdmin)
dogboarding_admin.register(Dog, DogAdmin)
dogboarding_admin.register(Kennel, KennelAdmin)
dogboarding_admin.register(Booking, BookingAdmin)
dogboarding_admin.register(DailyLog)
dogboarding_admin.register(Payment, PaymentAdmin)
dogboarding_admin.register(StaffNote, StaffNoteAdmin)
dogboarding_admin.register(FacilityAvailability, FacilityAvailabilityAdmin)

# Also register with default admin site for compatibility
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Dog, DogAdmin)
admin.site.register(Kennel, KennelAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(DailyLog)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(StaffNote, StaffNoteAdmin)
admin.site.register(FacilityAvailability, FacilityAvailabilityAdmin)
