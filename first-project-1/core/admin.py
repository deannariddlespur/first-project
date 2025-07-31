from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Owner, Dog, Kennel, Booking, DailyLog, Payment, StaffNote, FacilityAvailability

# Custom Admin Site
class DogBoardingAdminSite(AdminSite):
    site_header = "🐕 Dog Boarding Management"
    site_title = "Dog Boarding Admin"
    index_title = "Dashboard"
    site_url = "/"
    
    # Use custom admin templates
    index_template = "admin/base_site.html"
    app_index_template = "admin/base_site.html"
    
    def get_app_list(self, request):
        """
        Override to customize the admin app list
        """
        app_list = super().get_app_list(request)
        
        # Customize the app list for better organization
        for app in app_list:
            if app['app_label'] == 'core':
                app['name'] = '🐕 Dog Boarding'
                # Reorder models for better organization
                model_order = ['Owner', 'Dog', 'Booking', 'Kennel', 'Payment', 'StaffNote', 'FacilityAvailability', 'DailyLog']
                app['models'].sort(key=lambda x: model_order.index(x['name']) if x['name'] in model_order else 999)
        
        return app_list

# Create custom admin site instance
dogboarding_admin = DogBoardingAdminSite(name='dogboarding_admin')

# Custom Admin Classes
class BookingAdmin(admin.ModelAdmin):
    list_display = ['dog_display', 'owner_display', 'dates', 'status', 'kennel_display', 'total_display']
    list_filter = ['status', 'start_date', 'kennel__size']
    search_fields = ['dog__name', 'dog__owner__user__username', 'notes']
    date_hierarchy = 'start_date'
    readonly_fields = ['total_amount', 'price_per_night', 'nights']
    list_per_page = 25
    fieldsets = (
        ('Booking Details', {
            'fields': ('dog', 'start_date', 'end_date', 'status')
        }),
        ('Kennel Assignment', {
            'fields': ('kennel',),
            'classes': ('collapse',)
        }),
        ('Pricing', {
            'fields': ('total_amount', 'price_per_night', 'nights'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def dog_display(self, obj):
        return f"{obj.dog.name} ({obj.dog.breed or 'Mixed'})"
    dog_display.short_description = "Dog"
    
    def owner_display(self, obj):
        return obj.dog.owner.user.get_full_name() or obj.dog.owner.user.username
    owner_display.short_description = "Owner"
    
    def dates(self, obj):
        return f"{obj.start_date.strftime('%m/%d')} - {obj.end_date.strftime('%m/%d/%y')}"
    dates.short_description = "Dates"
    
    def kennel_display(self, obj):
        if obj.kennel:
            return f"{obj.kennel.name} ({obj.kennel.get_size_display()})"
        return "No kennel assigned"
    kennel_display.short_description = "Kennel"
    
    def total_display(self, obj):
        if obj.total_amount:
            return f"${obj.total_amount}"
        return "Not calculated"
    total_display.short_description = "Total"
    
    def nights(self, obj):
        return obj.get_nights()
    nights.short_description = "Nights"

class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed_display', 'age', 'size', 'owner_display', 'photo_status']
    list_filter = ['size', 'breed']
    search_fields = ['name', 'breed', 'owner__user__username', 'owner__user__first_name', 'owner__user__last_name']
    list_per_page = 20
    fieldsets = (
        ('Dog Information', {
            'fields': ('name', 'breed', 'age', 'size', 'notes')
        }),
        ('Owner', {
            'fields': ('owner',)
        }),
        ('Photo', {
            'fields': ('photo',),
            'classes': ('collapse',)
        }),
    )
    
    def breed_display(self, obj):
        return obj.breed if obj.breed else "Mixed breed"
    breed_display.short_description = "Breed"
    
    def owner_display(self, obj):
        return obj.owner.user.get_full_name() or obj.owner.user.username
    owner_display.short_description = "Owner"
    
    def photo_status(self, obj):
        if obj.photo:
            return "📸 Has photo"
        return "📷 No photo"
    photo_status.short_description = "Photo"

class KennelAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'description_short', 'current_status']
    list_filter = ['size']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Kennel Information', {
            'fields': ('name', 'size', 'description')
        }),
    )
    
    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "No description"
    description_short.short_description = "Description"
    
    def current_status(self, obj):
        # This is a simplified status - in real usage you'd check actual availability
        return "🟢 Available"
    current_status.short_description = "Status"

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking_display', 'amount_display', 'payment_method', 'status', 'created_date']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['booking__dog__name', 'booking__dog__owner__user__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_date']
    fieldsets = (
        ('Payment Information', {
            'fields': ('booking', 'amount', 'payment_method', 'status')
        }),
        ('Additional Info', {
            'fields': ('paid_date', 'notes'),
            'classes': ('collapse',)
        }),
        ('System Info', {
            'fields': ('created_date',),
            'classes': ('collapse',)
        }),
    )
    
    def booking_display(self, obj):
        return f"{obj.booking.dog.name} - {obj.booking.start_date.strftime('%m/%d')}"
    booking_display.short_description = "Booking"
    
    def amount_display(self, obj):
        return f"${obj.amount}"
    amount_display.short_description = "Amount"
    
    def created_date(self, obj):
        return obj.created_at.strftime('%B %d, %Y')
    created_date.short_description = "Created"

class StaffNoteAdmin(admin.ModelAdmin):
    list_display = ['booking_display', 'staff_member', 'note_preview', 'created_date']
    list_filter = ['created_at', 'staff_member']
    search_fields = ['note', 'booking__dog__name', 'staff_member__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_date']
    fieldsets = (
        ('Note Information', {
            'fields': ('booking', 'staff_member', 'note')
        }),
        ('Media', {
            'fields': ('picture',),
            'classes': ('collapse',)
        }),
        ('System Info', {
            'fields': ('created_date',),
            'classes': ('collapse',)
        }),
    )
    
    def booking_display(self, obj):
        return f"{obj.booking.dog.name} ({obj.booking.start_date.strftime('%m/%d')})"
    booking_display.short_description = "Booking"
    
    def note_preview(self, obj):
        if obj.note:
            return obj.note[:60] + "..." if len(obj.note) > 60 else obj.note
        return "No note"
    note_preview.short_description = "Note"
    
    def created_date(self, obj):
        return obj.created_at.strftime('%B %d, %Y')
    created_date.short_description = "Created"

class FacilityAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['date', 'type', 'title', 'description_short', 'created_by']
    list_filter = ['type', 'date', 'created_by']
    search_fields = ['title', 'description', 'created_by__username']
    date_hierarchy = 'date'
    readonly_fields = ['created_date']
    fieldsets = (
        ('Availability Information', {
            'fields': ('date', 'type', 'title', 'description')
        }),
        ('System Info', {
            'fields': ('created_by', 'created_date'),
            'classes': ('collapse',)
        }),
    )
    
    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "No description"
    description_short.short_description = "Description"
    
    def created_date(self, obj):
        return obj.created_at.strftime('%B %d, %Y')
    created_date.short_description = "Created"

class OwnerAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'phone', 'dog_count', 'created_date']
    list_filter = ['user__date_joined']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone']
    readonly_fields = ['created_date']
    fieldsets = (
        ('Owner Information', {
            'fields': ('user', 'phone', 'address')
        }),
        ('System Info', {
            'fields': ('created_date',),
            'classes': ('collapse',)
        }),
    )
    
    def user_display(self, obj):
        return f"{obj.user.get_full_name()} ({obj.user.username})"
    user_display.short_description = "Owner"
    
    def dog_count(self, obj):
        count = obj.dogs.count()
        return f"{count} dog{'s' if count != 1 else ''}"
    dog_count.short_description = "Dogs"
    
    def created_date(self, obj):
        return obj.user.date_joined.strftime('%B %d, %Y')
    created_date.short_description = "Joined"

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
