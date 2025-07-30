from django.contrib import admin
from django.utils.html import format_html
from .models import Owner, Dog, Kennel, Booking, DailyLog, Payment, StaffNote, FacilityAvailability

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['dog', 'owner', 'start_date', 'end_date', 'status', 'total_amount']
    list_filter = ['status', 'start_date', 'end_date']
    search_fields = ['dog__name', 'dog__owner__user__username']
    date_hierarchy = 'start_date'
    
    def owner(self, obj):
        return obj.dog.owner
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if form.base_fields.get('start_date'):
            form.base_fields['start_date'].widget.format = '%m/%d/%Y'
        if form.base_fields.get('end_date'):
            form.base_fields['end_date'].widget.format = '%m/%d/%Y'
        return form

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    date_hierarchy = 'created_at'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if form.base_fields.get('paid_date'):
            form.base_fields['paid_date'].widget.format = '%m/%d/%Y'
        return form

@admin.register(StaffNote)
class StaffNoteAdmin(admin.ModelAdmin):
    list_display = ['booking', 'staff_member', 'created_at', 'has_picture']
    list_filter = ['created_at', 'staff_member']
    search_fields = ['booking__dog__name', 'staff_member__username', 'note']
    date_hierarchy = 'created_at'
    
    def has_picture(self, obj):
        return bool(obj.picture)
    has_picture.boolean = True
    has_picture.short_description = 'Has Picture'

@admin.register(FacilityAvailability)
class FacilityAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['date', 'type', 'title', 'created_by', 'created_at']
    list_filter = ['type', 'date', 'created_at']
    search_fields = ['title', 'description', 'created_by__username']
    date_hierarchy = 'date'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if form.base_fields.get('date'):
            form.base_fields['date'].widget.format = '%m/%d/%Y'
        return form

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'breed', 'size', 'age']
    list_filter = ['size', 'age']
    search_fields = ['name', 'breed', 'owner__user__username']

admin.site.register(Owner)
admin.site.register(Kennel)
admin.site.register(DailyLog)
