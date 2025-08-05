import base64
from django.db import models
from django.contrib.auth.models import User
from .supabase_storage import supabase_storage

# Create your models here.

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Dog(models.Model):
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='dogs')
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='medium')
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to='dog_photos/', blank=True, null=True, max_length=500)
    # photo_url = models.URLField(blank=True, null=True)  # Removed permanently
    # supabase_url = models.URLField(blank=True, null=True, max_length=1000)  # Temporarily commented out

    def __str__(self):
        return f"{self.name} ({self.owner}) - {self.get_size_display()}"
    
    def get_photo_url(self):
        """Get photo URL with comprehensive fallback system"""
        # Try to get Supabase URL from photo field
        try:
            if self.photo and self.photo.name:
                # Check if this is a Supabase URL (stored in photo field)
                if self.photo.name.startswith('http'):
                    print(f"✅ Using Supabase photo URL for {self.name}: {self.photo.name}")
                    return self.photo.name
        except Exception as e:
            print(f"⚠️ Supabase photo not available for {self.name}: {e}")
        
        # Try local photo as fallback
        try:
            if self.photo:
                photo_url = self.photo.url
                print(f"✅ Using local photo URL for {self.name}: {photo_url}")
                return photo_url
        except Exception as e:
            print(f"⚠️ Local photo not available for {self.name}: {e}")
        
        # Fallback to a placeholder
        placeholder_url = f"https://via.placeholder.com/300x300/667eea/ffffff?text={self.name}"
        print(f"✅ Using placeholder URL for {self.name}: {placeholder_url}")
        return placeholder_url
    
    def save_photo_to_supabase(self, image_file):
        """Upload photo to Supabase for persistent storage"""
        debug_info = {
            'image_file_name': image_file.name,
            'image_file_size': image_file.size,
            'supabase_upload_result': None,
            'error': None,
            'error_type': None
        }
        
        try:
            print(f"🔄 Uploading photo for {self.name} to Supabase...")
            print(f"🔍 Image file name: {image_file.name}")
            print(f"🔍 Image file size: {image_file.size}")
            
            # Upload to Supabase
            public_url = supabase_storage.upload_file(image_file)
            debug_info['supabase_upload_result'] = public_url
            print(f"🔍 Supabase upload result: {public_url}")
            
            if public_url and public_url.startswith('http'):
                print(f"✅ Photo uploaded successfully: {public_url}")
                # Store the Supabase URL in the photo field
                try:
                    # Store Supabase URL in the photo field name (truncated if needed)
                    # The photo field now has max_length=500, so this should work
                    self.photo.name = public_url
                    self.save()
                    return True, debug_info
                except Exception as save_error:
                    print(f"❌ Error saving Supabase URL to database: {save_error}")
                    debug_info['error'] = f"Database save error: {save_error}"
                    debug_info['error_type'] = str(type(save_error))
                    # Fallback to local storage
                    self.photo.save(image_file.name, image_file, save=True)
                    return False, debug_info
            else:
                print(f"❌ Supabase upload failed for {self.name}, falling back to local storage")
                print(f"🔍 Public URL was: {public_url}")
                debug_info['error'] = f"Supabase upload returned: {public_url}"
                # Fallback to local storage
                self.photo.save(image_file.name, image_file, save=True)
                return False, debug_info
                
        except Exception as e:
            print(f"❌ Error in save_photo_to_supabase for {self.name}: {e}")
            print(f"🔍 Error type: {type(e)}")
            print(f"🔍 Error details: {str(e)}")
            debug_info['error'] = str(e)
            debug_info['error_type'] = str(type(e))
            # Fallback to local storage
            self.photo.save(image_file.name, image_file, save=True)
            return False, debug_info


class Kennel(models.Model):
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='medium')

    def __str__(self):
        return self.name
    
    def is_available_for_dates(self, start_date, end_date, exclude_booking=None):
        """Check if kennel is available for the given date range"""
        conflicting_bookings = Booking.objects.filter(
            kennel=self,
            start_date__lte=end_date,
            end_date__gte=start_date,
            status__in=['pending', 'confirmed']
        )
        
        if exclude_booking:
            conflicting_bookings = conflicting_bookings.exclude(id=exclude_booking.id)
        
        return not conflicting_bookings.exists()
    
    def get_conflicting_bookings(self, start_date, end_date, exclude_booking=None):
        """Get bookings that conflict with the given date range"""
        conflicting_bookings = Booking.objects.filter(
            kennel=self,
            start_date__lte=end_date,
            end_date__gte=start_date,
            status__in=['pending', 'confirmed']
        )
        
        if exclude_booking:
            conflicting_bookings = conflicting_bookings.exclude(id=exclude_booking.id)
        
        return conflicting_bookings

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='bookings')
    kennel = models.ForeignKey(Kennel, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    # Pricing fields
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.dog} ({self.start_date} to {self.end_date})"
    
    def calculate_total(self):
        """Calculate total amount based on kennel size and length of stay"""
        if not self.dog or not self.start_date or not self.end_date:
            return 0
        
        # Calculate number of nights
        nights = (self.end_date - self.start_date).days
        
        # Determine price based on kennel size if assigned, otherwise dog size
        if self.kennel:
            # Use kennel size for pricing
            if self.kennel.size == 'small':
                price_per_night = 50
            elif self.kennel.size == 'medium':
                price_per_night = 75
            elif self.kennel.size == 'large':
                price_per_night = 100
            else:
                price_per_night = 75  # Default to medium price
        else:
            # Fallback to dog size-based pricing
            if self.dog.size == 'large':
                price_per_night = 100
            elif self.dog.size == 'medium':
                price_per_night = 75
            else:
                price_per_night = 50   # Small dog price
        
        total = nights * price_per_night
        self.price_per_night = price_per_night
        self.total_amount = total
        return total
    
    def recalculate_pricing(self):
        """Recalculate and save pricing for this booking"""
        total = self.calculate_total()
        self.save()
        return total
    
    def get_nights(self):
        """Get number of nights for this booking"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return 0
    
    def is_kennel_appropriate_for_dog(self):
        """Check if the assigned kennel is appropriate for the dog's size"""
        if not self.kennel or not self.dog:
            return True  # No kennel assigned or no dog, so no size conflict
        
        # Size compatibility rules
        size_compatibility = {
            'small': ['small', 'medium', 'large'],    # Small dogs can use any kennel
            'medium': ['medium', 'large'],            # Medium dogs need medium or large
            'large': ['large']                        # Large dogs need large kennels only
        }
        
        dog_size = self.dog.size
        kennel_size = self.kennel.size
        
        return kennel_size in size_compatibility.get(dog_size, ['large'])
    
    def get_appropriate_kennels(self, start_date, end_date):
        """Get kennels that are both available and appropriate for the dog's size"""
        from .models import Kennel
        
        # Get all available kennels for the date range
        available_kennels = []
        for kennel in Kennel.objects.all():
            if kennel.is_available_for_dates(start_date, end_date, self):
                available_kennels.append(kennel)
        
        # Filter by size appropriateness
        appropriate_kennels = []
        for kennel in available_kennels:
            # Create a temporary booking to check compatibility
            temp_booking = Booking(dog=self.dog, kennel=kennel)
            if temp_booking.is_kennel_appropriate_for_dog():
                appropriate_kennels.append(kennel)
        
        return appropriate_kennels

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('check', 'Check'),
        ('online', 'Online Payment'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    paid_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for {self.booking} - ${self.amount}"
    
    def mark_as_paid(self, payment_method='cash'):
        """Mark payment as paid"""
        from django.utils import timezone
        self.status = 'paid'
        self.payment_method = payment_method
        self.paid_date = timezone.now()
        self.save()

class DailyLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    feeding = models.TextField(blank=True)
    medication = models.TextField(blank=True)
    exercise = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to='daily_logs/', blank=True, null=True)

    def __str__(self):
        return f"Log for {self.booking.dog} on {self.date}"

class StaffNote(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='staff_notes')
    staff_member = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    picture = models.ImageField(upload_to='staff_notes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Staff note for {self.booking.dog} by {self.staff_member}"

class FacilityAvailability(models.Model):
    TYPE_CHOICES = [
        ('closed', 'Facility Closed'),
        ('vacation', 'Staff Vacation'),
        ('maintenance', 'Maintenance'),
        ('holiday', 'Holiday'),
        ('limited', 'Limited Hours'),
        ('other', 'Other'),
    ]
    
    date = models.DateField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Facility Availability"
        ordering = ['date']
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.title} ({self.date})"
    
    @classmethod
    def is_facility_closed(cls, date):
        """Check if facility is closed on a specific date"""
        return cls.objects.filter(date=date, type='closed').exists()
    
    @classmethod
    def get_availability_for_month(cls, year, month):
        """Get all availability entries for a specific month"""
        from datetime import date
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        return cls.objects.filter(date__gte=start_date, date__lt=end_date)
