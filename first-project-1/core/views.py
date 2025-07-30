from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Owner
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Dog
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Booking
from .models import Kennel
from .models import Payment
import time
from .models import StaffNote
from django.contrib import admin
from django.utils.html import format_html
from .models import Owner, Dog, Kennel, Booking, DailyLog, Payment, StaffNote
from django import forms
from .models import FacilityAvailability
from django.core.exceptions import ValidationError
from django.contrib import messages

def home(request):
    """Homepage view - landing page for the dog boarding system"""
    return render(request, 'core/home.html')

class AdminUserForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter first name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}))
    is_staff = forms.BooleanField(required=False, initial=True)
    is_superuser = forms.BooleanField(required=False, initial=True)

def create_admin_user(request):
    """Simple view to create admin users"""
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            try:
                # Check if user already exists
                if User.objects.filter(username=form.cleaned_data['username']).exists():
                    messages.error(request, f"User '{form.cleaned_data['username']}' already exists!")
                else:
                    # Create the user
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        is_staff=form.cleaned_data['is_staff'],
                        is_superuser=form.cleaned_data['is_superuser']
                    )
                    messages.success(request, f"✅ Admin user '{user.username}' created successfully!")
                    return redirect('create_admin_user')
            except Exception as e:
                messages.error(request, f"Error creating user: {str(e)}")
    else:
        form = AdminUserForm()
    
    # Get list of existing users (with error handling)
    try:
        existing_users = User.objects.all().order_by('username')
    except Exception as e:
        existing_users = []
        messages.error(request, f"Database error: {str(e)}. Please run migrations first.")
    
    return render(request, 'core/create_admin_user.html', {
        'form': form,
        'existing_users': existing_users
    })

def setup_database(request):
    """Simple view to run database setup"""
    from django.core.management import execute_from_command_line
    import sys
    
    if request.method == 'POST':
        try:
            # Run migrations
            execute_from_command_line(['manage.py', 'migrate'])
            messages.success(request, "✅ Database migrations completed successfully!")
            
            # Create a default admin user
            if not User.objects.filter(username='admin').exists():
                admin_user = User.objects.create_user(
                    username='admin',
                    email='admin@dogboarding.com',
                    password='admin123456',
                    first_name='Admin',
                    last_name='User',
                    is_staff=True,
                    is_superuser=True
                )
                messages.success(request, f"✅ Default admin user created: username='admin', password='admin123456'")
            
            # Create some sample kennels
            from .models import Kennel
            if not Kennel.objects.exists():
                kennel_data = [
                    {'name': 'Kennel 001', 'description': 'Small kennel for small dogs', 'size': 'small'},
                    {'name': 'Kennel 002', 'description': 'Medium kennel for medium dogs', 'size': 'medium'},
                    {'name': 'Kennel 003', 'description': 'Large kennel for large dogs', 'size': 'large'},
                    {'name': 'Kennel 004', 'description': 'Small kennel for small dogs', 'size': 'small'},
                    {'name': 'Kennel 005', 'description': 'Medium kennel for medium dogs', 'size': 'medium'},
                    {'name': 'Kennel 006', 'description': 'Large kennel for large dogs', 'size': 'large'},
                ]
                
                for kennel_info in kennel_data:
                    Kennel.objects.create(**kennel_info)
                
                messages.success(request, "✅ Sample kennels created!")
            
            return redirect('setup_database')
            
        except Exception as e:
            messages.error(request, f"Error setting up database: {str(e)}")
    
    return render(request, 'core/setup_database.html')

class KennelForm(forms.ModelForm):
    class Meta:
        model = Kennel
        fields = ['name', 'description', 'size']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Kennel 003'}),
            'description': forms.Textarea(attrs={'placeholder': 'e.g., For Medium Dogs', 'rows': 3}),
            'size': forms.Select(attrs={'class': 'form-control'}),
        }

class FacilityAvailabilityForm(forms.ModelForm):
    class Meta:
        model = FacilityAvailability
        fields = ['date', 'type', 'title', 'description']
        widgets = {
            'date': forms.TextInput(
                attrs={
                    'type': 'text',
                    'placeholder': 'mm/dd/yyyy',
                    'pattern': r'\d{2}/\d{2}/\d{4}',
                    'class': 'date-input'
                }
            ),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Christmas Holiday'}),
            'description': forms.Textarea(attrs={'placeholder': 'Additional details...', 'rows': 3}),
        }

class OwnerRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Owner
        fields = ['phone', 'address']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        owner = super().save(commit=False)
        owner.user = user
        if commit:
            owner.save()
        return owner

def register_owner(request):
    if request.method == 'POST':
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            owner = form.save()
            login(request, owner.user)  # Log in the new user
            return redirect('owner_dashboard')
    else:
        form = OwnerRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def login_owner(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('owner_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

class DogForm(ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'breed', 'age', 'size', 'notes', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Buddy'}),
            'breed': forms.TextInput(attrs={'placeholder': 'e.g., Golden Retriever'}),
            'age': forms.NumberInput(attrs={'placeholder': 'e.g., 3'}),
            'size': forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%; padding: 8px; border: 1px solid #f7d08a; border-radius: 4px;'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Any special needs or notes', 'rows': 3}),
        }

@login_required
def owner_dashboard(request):
    owner = get_object_or_404(Owner, user=request.user)
    dogs = owner.dogs.all()
    return render(request, 'core/dashboard.html', {'dogs': dogs})

@login_required
def add_dog(request):
    owner = get_object_or_404(Owner, user=request.user)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save(commit=False)
            dog.owner = owner
            dog.save()
            return redirect('owner_dashboard')
    else:
        form = DogForm()
    return render(request, 'core/add_dog.html', {'form': form})

@login_required
def edit_dog(request, dog_id):
    owner = get_object_or_404(Owner, user=request.user)
    dog = get_object_or_404(Dog, id=dog_id, owner=owner)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            return redirect('owner_dashboard')
    else:
        form = DogForm(instance=dog)
    return render(request, 'core/edit_dog.html', {'form': form, 'dog': dog})

@login_required
def delete_dog(request, dog_id):
    owner = get_object_or_404(Owner, user=request.user)
    dog = get_object_or_404(Dog, id=dog_id, owner=owner)
    if request.method == 'POST':
        dog.delete()
        return redirect('owner_dashboard')
    return render(request, 'core/delete_dog.html', {'dog': dog})

class BookingForm(forms.ModelForm):
    # Add dog size field for booking
    dog_size = forms.ChoiceField(
        choices=[
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; border: 1px solid #f7d08a; border-radius: 4px;'
        })
    )
    
    class Meta:
        model = Booking
        fields = ['dog', 'start_date', 'end_date', 'notes']
        widgets = {
            'start_date': forms.TextInput(
                attrs={
                    'type': 'text',
                    'placeholder': 'mm/dd/yyyy',
                    'pattern': r'\d{2}/\d{2}/\d{4}',
                    'class': 'date-input'
                }
            ),
            'end_date': forms.TextInput(
                attrs={
                    'type': 'text',
                    'placeholder': 'mm/dd/yyyy',
                    'pattern': r'\d{2}/\d{2}/\d{4}',
                    'class': 'date-input'
                }
            ),
        }

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dog'].queryset = owner.dogs.all()
        
        # Set date format for display
        self.fields['start_date'].input_formats = ['%m/%d/%Y', '%Y-%m-%d', '%m/%d/%y']
        self.fields['end_date'].input_formats = ['%m/%d/%Y', '%Y-%m-%d', '%m/%d/%y']
        
        # Set initial dog size if dog is selected
        if self.instance and hasattr(self.instance, 'dog') and self.instance.dog:
            self.fields['dog_size'].initial = self.instance.dog.size

    def clean(self):
        cleaned_data = super().clean()
        dog = cleaned_data.get('dog')
        kennel_id = self.data.get('kennel') if self.data else None
        
        if dog and kennel_id:
            try:
                kennel = Kennel.objects.get(id=kennel_id)
                size_compatibility = {
                    'small': ['small', 'medium', 'large'],
                    'medium': ['medium', 'large'],
                    'large': ['large']
                }
                if kennel.size not in size_compatibility.get(dog.size, ['large']):
                    raise ValidationError(f"A {dog.get_size_display()} dog cannot be placed in a {kennel.get_size_display()} kennel.")
            except Kennel.DoesNotExist:
                pass
        return cleaned_data

@login_required
def booking_calendar(request):
    # Get year and month from URL parameters, default to current month
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    # Handle month/year transitions
    if month == 0:
        month = 12
        year -= 1
    elif month == 13:
        month = 1
        year += 1
    
    # Calculate previous and next month/year
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year = year - 1
    
    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year = year + 1
    
    # Get the first day of the month and the last day
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Get the day of the week for the first day (0 = Monday, 6 = Sunday)
    first_day_weekday = first_day.weekday()
    
    # Adjust for Sunday start (0 = Sunday, 6 = Saturday)
    first_day_weekday = (first_day_weekday + 1) % 7
    
    # Calculate the start of the calendar (first Sunday)
    calendar_start = first_day - timedelta(days=first_day_weekday)
    
    # Get all kennels for availability calculation
    kennels = Kennel.objects.all()
    
    # Get all bookings for the current month
    month_start = first_day.date()
    month_end = last_day.date()
    bookings = Booking.objects.filter(
        start_date__lte=month_end,
        end_date__gte=month_start
    )
    
    # Create calendar weeks
    calendar_weeks = []
    current_date = calendar_start
    
    for week in range(6):  # 6 weeks to ensure we cover the entire month
        week_days = []
        for day in range(7):
            if current_date.month == month:
                # Check availability for this day
                day_date = current_date.date()
                available_kennels = []
                total_kennels = kennels.count()
                
                for kennel in kennels:
                    if kennel.is_available_for_dates(day_date, day_date):
                        available_kennels.append(kennel)
                
                # Calculate availability percentage
                availability_percentage = (len(available_kennels) / total_kennels * 100) if total_kennels > 0 else 0
                
                # Check if there are any bookings for this day
                day_bookings = bookings.filter(
                    start_date__lte=day_date,
                    end_date__gte=day_date
                )
                
                week_days.append({
                    'date': current_date,
                    'is_today': current_date.date() == timezone.now().date(),
                    'is_other_month': False,
                    'has_booking': day_bookings.exists(),
                    'booking_count': day_bookings.count(),
                    'available_kennels': len(available_kennels),
                    'total_kennels': total_kennels,
                    'availability_percentage': availability_percentage,
                    'availability_status': 'high' if availability_percentage >= 70 else 'medium' if availability_percentage >= 30 else 'low'
                })
            else:
                week_days.append({
                    'date': current_date,
                    'is_today': False,
                    'is_other_month': True,
                    'has_booking': False,
                    'booking_count': 0,
                    'available_kennels': 0,
                    'total_kennels': 0,
                    'availability_percentage': 0,
                    'availability_status': 'none'
                })
            current_date += timedelta(days=1)
        calendar_weeks.append(week_days)
    
    context = {
        'year': year,
        'month': month,
        'calendar_weeks': calendar_weeks,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'total_kennels': kennels.count(),
    }
    return render(request, 'core/booking_calendar.html', context)

@login_required
def create_booking(request):
    owner = get_object_or_404(Owner, user=request.user)
    
    if request.method == 'POST':
        form = BookingForm(owner, request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.dog = form.cleaned_data['dog']
            
            # Update dog size if provided
            dog_size = form.cleaned_data.get('dog_size')
            if dog_size and booking.dog:
                booking.dog.size = dog_size
                booking.dog.save()
            
            # Check if a kennel is selected and if it's available and appropriate
            kennel_id = request.POST.get('kennel')
            if kennel_id:
                try:
                    kennel = Kennel.objects.get(id=kennel_id)
                    
                    # Check availability
                    if not kennel.is_available_for_dates(booking.start_date, booking.end_date):
                        form.add_error(None, f"Kennel {kennel.name} is not available for the selected dates.")
                        # Get appropriate kennels for the selected dates
                        appropriate_kennels = booking.get_appropriate_kennels(booking.start_date, booking.end_date)
                        return render(request, 'core/create_booking.html', {
                            'form': form,
                            'available_kennels': appropriate_kennels,
                            'all_kennels': Kennel.objects.all()
                        })
                    
                    # Check size compatibility using the form's dog size
                    dog_size = form.cleaned_data.get('dog_size', booking.dog.size if booking.dog else 'medium')
                    
                    # Size compatibility rules
                    size_compatibility = {
                        'small': ['small', 'medium', 'large'],    # Small dogs can use any kennel
                        'medium': ['medium', 'large'],            # Medium dogs need medium or large
                        'large': ['large']                        # Large dogs need large kennels only
                    }
                    
                    if kennel.size not in size_compatibility.get(dog_size, ['large']):
                        form.add_error(None, f"Kennel {kennel.name} ({kennel.get_size_display()}) is not appropriate for a {dog_size} dog.")
                        # Get appropriate kennels for the selected dates
                        appropriate_kennels = []
                        for k in Kennel.objects.all():
                            if k.is_available_for_dates(booking.start_date, booking.end_date) and k.size in size_compatibility.get(dog_size, ['large']):
                                appropriate_kennels.append(k)
                        return render(request, 'core/create_booking.html', {
                            'form': form,
                            'available_kennels': appropriate_kennels,
                            'all_kennels': Kennel.objects.all()
                        })
                    
                    booking.kennel = kennel
                    # Recalculate pricing when kennel is assigned
                    booking.recalculate_pricing()
                except Kennel.DoesNotExist:
                    form.add_error(None, "Selected kennel does not exist.")
                    return render(request, 'core/create_booking.html', {
                        'form': form,
                        'all_kennels': Kennel.objects.all()
                    })
            
            # Calculate pricing
            total_amount = booking.calculate_total()
            booking.save()
            
            # Create payment record
            Payment.objects.create(
                booking=booking,
                amount=total_amount,
                status='pending'
            )
            
            return redirect('booking_list')
    else:
        # Handle pre-filling dates from URL parameters
        initial_data = {}
        if request.GET.get('start_date') and request.GET.get('end_date'):
            try:
                start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
                end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
                initial_data = {
                    'start_date': start_date.strftime('%m/%d/%Y'),
                    'end_date': end_date.strftime('%m/%d/%Y')
                }
            except ValueError:
                pass
        
        form = BookingForm(owner, initial=initial_data)
    
    # Get all kennels for initial display
    all_kennels = Kennel.objects.all()
    
    # Get appropriate kennels for the current date range (if dates are selected)
    available_kennels = []
    if request.GET.get('start_date') and request.GET.get('end_date'):
        try:
            start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
            
            # Check if a dog is selected in the form data
            selected_dog_id = request.GET.get('dog') or (form.data.get('dog') if form.data else None)
            if selected_dog_id:
                try:
                    selected_dog = Dog.objects.get(id=selected_dog_id)
                    size_compatibility = {
                        'small': ['small', 'medium', 'large'],
                        'medium': ['medium', 'large'],
                        'large': ['large']
                    }
                    for kennel in all_kennels:
                        if (
                            kennel.is_available_for_dates(start_date, end_date)
                            and kennel.size in size_compatibility.get(selected_dog.size, ['large'])
                        ):
                            available_kennels.append(kennel)
                except Dog.DoesNotExist:
                    pass
            else:
                # If no dog selected, show all available kennels
                for kennel in all_kennels:
                    if kennel.is_available_for_dates(start_date, end_date):
                        available_kennels.append(kennel)
        except ValueError:
            pass
    
    return render(request, 'core/create_booking.html', {
        'form': form,
        'available_kennels': available_kennels,
        'all_kennels': all_kennels,
        'cache_buster': int(time.time())  # Force cache refresh
    })

@login_required
def booking_list(request):
    owner = get_object_or_404(Owner, user=request.user)
    
    # Get filter parameter
    status_filter = request.GET.get('status', 'all')
    
    # Get all bookings for this owner
    bookings = Booking.objects.filter(dog__owner=owner).order_by('-created_at')
    
    # Apply status filter if not 'all'
    if status_filter != 'all':
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'status_choices': [('all', 'All Bookings')] + list(Booking.STATUS_CHOICES),
        'current_filter': status_filter,
    }
    return render(request, 'core/booking_list.html', context)

@login_required
def cancel_booking(request, booking_id):
    owner = get_object_or_404(Owner, user=request.user)
    booking = get_object_or_404(Booking, id=booking_id, dog__owner=owner)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        return redirect('booking_list')
    
    return render(request, 'core/cancel_booking.html', {'booking': booking})

def is_staff(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_staff)
def staff_dashboard(request):
    # Get filter parameters
    filter_month = request.GET.get('month', timezone.now().month)
    filter_year = request.GET.get('year', timezone.now().year)
    
    try:
        filter_month = int(filter_month)
        filter_year = int(filter_year)
    except (ValueError, TypeError):
        filter_month = timezone.now().month
        filter_year = timezone.now().year
    
    # Calculate date range for filtering
    if filter_month == 12:
        next_month = 1
        next_year = filter_year + 1
    else:
        next_month = filter_month + 1
        next_year = filter_year
    
    start_date = datetime(filter_year, filter_month, 1).date()
    end_date = datetime(next_year, next_month, 1).date() - timedelta(days=1)
    
    # Get all bookings for the filtered period
    # Filter by booking dates (when the stay occurs), not when booking was created
    bookings = Booking.objects.filter(
        start_date__lte=end_date,
        end_date__gte=start_date
    ).order_by('start_date')
    
    # Get upcoming bookings (next 7 days) - only confirmed bookings
    # Pending bookings should only appear in the "Pending Bookings" section
    today = timezone.now().date()
    upcoming_bookings = Booking.objects.filter(
        start_date__gte=today,
        status='confirmed'
    ).order_by('start_date')[:10]
    
    # Get pending bookings for the filtered period
    # These are bookings that need staff attention/confirmation
    pending_bookings = bookings.filter(status='pending')
    
    # Get kennel assignments
    kennels = Kennel.objects.all()
    
    # Calculate payment statistics for the filtered period
    # Get payments for bookings that occur during the filtered period
    payments = Payment.objects.filter(
        booking__start_date__lte=end_date,
        booking__end_date__gte=start_date
    )
    total_revenue = sum(payment.amount for payment in payments.filter(status='paid'))
    pending_payments = sum(payment.amount for payment in payments.filter(status='pending'))
    
    # Get all bookings for total count (not filtered by period)
    all_bookings = Booking.objects.all()
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'pending_bookings': pending_bookings,
        'kennels': kennels,
        'total_bookings': all_bookings.count(),
        'filtered_bookings': bookings.count(),
        'total_pending': pending_bookings.count(),
        'total_revenue': total_revenue,
        'pending_payments': pending_payments,
        'filter_month': filter_month,
        'filter_year': filter_year,
        'start_date': start_date,
        'end_date': end_date,
        'month_name': datetime(filter_year, filter_month, 1).strftime('%B %Y'),
    }
    return render(request, 'core/staff_dashboard.html', context)

@user_passes_test(is_staff)
def staff_booking_list(request):
    # Get filter parameter
    status_filter = request.GET.get('status', 'all')
    
    # Get all bookings
    bookings = Booking.objects.all().order_by('-created_at')
    
    # Apply status filter
    if status_filter != 'all':
        bookings = bookings.filter(status=status_filter)
    
    # Get all status choices for the filter dropdown
    status_choices = [('all', 'All Bookings')] + list(Booking.STATUS_CHOICES)
    
    context = {
        'bookings': bookings,
        'status_choices': status_choices,
        'current_filter': status_filter,
    }
    return render(request, 'core/staff_booking_list.html', context)

@user_passes_test(is_staff)
def staff_booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        # Update booking status
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            # Clear kennel assignment when status is changed to pending
            if new_status == 'pending':
                booking.kennel = None
        
        # Assign kennel with availability check
        kennel_id = request.POST.get('kennel')
        if kennel_id:
            try:
                kennel = Kennel.objects.get(id=kennel_id)
                if not kennel.is_available_for_dates(booking.start_date, booking.end_date, booking):
                    # Add error message but don't save the kennel assignment
                    pass
                else:
                    # Check size compatibility
                    size_compatibility = {
                        'small': ['small', 'medium', 'large'],
                        'medium': ['medium', 'large'],
                        'large': ['large']
                    }
                    if kennel.size not in size_compatibility.get(booking.dog.size, ['large']):
                        # Add error message but don't save the kennel assignment
                        pass
                    else:
                        booking.kennel = kennel
                        # Recalculate pricing when kennel changes
                        booking.recalculate_pricing()
            except Kennel.DoesNotExist:
                pass
        
        booking.save()
        
        # Handle staff note creation
        staff_note = request.POST.get('staff_note')
        staff_picture = request.FILES.get('staff_picture')
        
        if staff_note or staff_picture:
            StaffNote.objects.create(
                booking=booking,
                staff_member=request.user,
                note=staff_note or '',
                picture=staff_picture
            )
        
        return redirect('staff_booking_detail', booking_id=booking_id)
    
    # Get available kennels for this booking's dates
    available_kennels = []
    all_kennels = Kennel.objects.all()
    
    # Size compatibility rules
    size_compatibility = {
        'small': ['small', 'medium', 'large'],
        'medium': ['medium', 'large'],
        'large': ['large']
    }
    
    for kennel in all_kennels:
        if kennel.is_available_for_dates(booking.start_date, booking.end_date, booking):
            # Only include kennels appropriate for the dog's size
            if kennel.size in size_compatibility.get(booking.dog.size, ['large']):
                available_kennels.append(kennel)
        elif booking.kennel == kennel:
            # Include current kennel even if it would conflict (for editing)
            available_kennels.append(kennel)
    
    # Get existing staff notes for this booking
    staff_notes = booking.staff_notes.all().order_by('-created_at')
    
    return render(request, 'core/staff_booking_detail.html', {
        'booking': booking,
        'available_kennels': available_kennels,
        'all_kennels': all_kennels,
        'staff_notes': staff_notes,
    })

@user_passes_test(is_staff)
def staff_kennel_management(request):
    if request.method == 'POST':
        form = KennelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_kennel_management')
    else:
        form = KennelForm()
    
    # Get filter parameters
    size_filter = request.GET.get('size', 'all')
    availability_filter = request.GET.get('availability', 'all')
    
    kennels = Kennel.objects.all()
    
    # Apply size filter
    if size_filter != 'all':
        kennels = kennels.filter(size=size_filter)
    
    # Get bookings for each kennel and apply availability filter
    for kennel in kennels:
        kennel.current_bookings = Booking.objects.filter(
            kennel=kennel,
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date(),
            status__in=['confirmed', 'pending']
        )
    
    # Apply availability filter
    if availability_filter == 'available':
        kennels = [kennel for kennel in kennels if not kennel.current_bookings]
    elif availability_filter == 'occupied':
        kennels = [kennel for kennel in kennels if kennel.current_bookings]
    
    return render(request, 'core/staff_kennel_management.html', {
        'kennels': kennels,
        'form': form,
        'size_filter': size_filter,
        'availability_filter': availability_filter,
        'size_choices': Kennel.SIZE_CHOICES,
    })

@user_passes_test(is_staff)
def edit_kennel(request, kennel_id):
    """Staff view to edit kennel information"""
    kennel = get_object_or_404(Kennel, id=kennel_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        size = request.POST.get('size', 'medium')
        
        if name and size in ['small', 'medium', 'large']:
            kennel.name = name
            kennel.description = description
            kennel.size = size
            kennel.save()
        
        return redirect('staff_kennel_management')
    
    return redirect('staff_kennel_management')

def staff_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('staff_dashboard')
            else:
                form.add_error(None, "This login is for staff only. Dog owners should use the main login page.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/staff_login.html', {'form': form})

@user_passes_test(is_staff)
def staff_payment_list(request):
    """Staff view to manage all payments"""
    payments = Payment.objects.all().order_by('-created_at')
    
    # Get filter parameter
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        payments = payments.filter(status=status_filter)
    
    context = {
        'payments': payments,
        'status_choices': [('all', 'All Payments')] + list(Payment.PAYMENT_STATUS_CHOICES),
        'current_filter': status_filter,
    }
    return render(request, 'core/staff_payment_list.html', context)

@user_passes_test(is_staff)
def staff_payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'mark_paid':
            payment_method = request.POST.get('payment_method', 'cash')
            payment.mark_as_paid(payment_method)
            return redirect('staff_payment_list')
        elif action == 'mark_pending':
            payment.status = 'pending'
            payment.save()
        elif action == 'mark_overdue':
            payment.status = 'overdue'
            payment.save()
        elif action == 'mark_cancelled':
            payment.status = 'cancelled'
            payment.save()
        elif action == 'update_only':
            payment_method = request.POST.get('payment_method')
            if payment_method:
                payment.payment_method = payment_method
                payment.save()
        
        return redirect('staff_payment_detail', payment_id=payment.id)
    
    context = {
        'payment': payment,
        'payment_methods': Payment.PAYMENT_METHOD_CHOICES,
    }
    return render(request, 'core/staff_payment_detail.html', context)

@user_passes_test(is_staff)
def staff_calendar(request):
    # Handle POST request for adding/editing availability entry
    if request.method == 'POST':
        entry_id = request.POST.get('entry_id')
        
        # Check for booking conflicts before processing
        date_str = request.POST.get('date')
        entry_type = request.POST.get('type')
        
        if date_str and entry_type in ['closed', 'maintenance']:
            try:
                # Convert date string to date object
                from datetime import datetime
                selected_date = datetime.strptime(date_str, '%m/%d/%Y').date()
                
                # Check for confirmed bookings on this date
                conflicting_bookings = Booking.objects.filter(
                    start_date__lte=selected_date,
                    end_date__gte=selected_date,
                    status='confirmed'
                )
                
                if conflicting_bookings.exists():
                    # Add error message to context
                    error_message = f"Cannot set facility as '{entry_type}' on {date_str} - there are confirmed bookings on this date."
                    context = {
                        'year': int(request.GET.get('year', timezone.now().year)),
                        'month': int(request.GET.get('month', timezone.now().month)),
                        'calendar_weeks': [],  # Will be filled by the rest of the view
                        'error_message': error_message,
                    }
                    # Rebuild calendar context and return with error
                    return _build_calendar_context(request, context)
            except ValueError:
                pass  # Invalid date format, let form validation handle it
        
        if entry_id:
            # Editing existing entry
            entry = get_object_or_404(FacilityAvailability, id=entry_id)
            
            # Check if we're changing to a conflicting type
            if entry_type in ['closed', 'maintenance']:
                try:
                    # Convert date string to date object
                    from datetime import datetime
                    selected_date = datetime.strptime(date_str, '%m/%d/%Y').date()
                    
                    # Check for confirmed bookings on this date
                    conflicting_bookings = Booking.objects.filter(
                        start_date__lte=selected_date,
                        end_date__gte=selected_date,
                        status='confirmed'
                    )
                    
                    if conflicting_bookings.exists():
                        # Add error message to context
                        error_message = f"Cannot change availability to '{entry_type}' on {date_str} - there are confirmed bookings on this date."
                        context = {
                            'year': int(request.GET.get('year', timezone.now().year)),
                            'month': int(request.GET.get('month', timezone.now().month)),
                            'calendar_weeks': [],  # Will be filled by the rest of the view
                            'error_message': error_message,
                        }
                        # Rebuild calendar context and return with error
                        return _build_calendar_context(request, context)
                except ValueError:
                    pass  # Invalid date format, let form validation handle it
            
            form = FacilityAvailabilityForm(request.POST, instance=entry)
        else:
            # Adding new entry
            form = FacilityAvailabilityForm(request.POST)
        
        if form.is_valid():
            availability = form.save(commit=False)
            if not entry_id:  # Only set created_by for new entries
                availability.created_by = request.user
            availability.save()
            print(f"DEBUG: Saved availability with type: {availability.type}")  # Debug line
            
            # Redirect back to the same month/year
            year = int(request.GET.get('year', timezone.now().year))
            month = int(request.GET.get('month', timezone.now().month))
            from django.urls import reverse
            return redirect(f"{reverse('staff_calendar')}?year={year}&month={month}")
        else:
            print(f"DEBUG: Form errors: {form.errors}")  # Debug line
            # If form is invalid, we'll need to handle this in the template
            pass
    
    # Build calendar context
    context = _build_calendar_context(request, {})
    return render(request, 'core/staff_calendar.html', context)

def _build_calendar_context(request, context):
    """Helper function to build calendar context"""
    # Get year and month from URL parameters, default to current month
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    # Handle month/year transitions
    if month == 0:
        month = 12
        year -= 1
    elif month == 13:
        month = 1
        year += 1
    
    # Calculate previous and next month/year
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year = year - 1
    
    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year = year + 1
    
    # Get the first day of the month and the last day
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Get the day of the week for the first day (0 = Monday, 6 = Sunday)
    first_day_weekday = first_day.weekday()
    
    # Adjust for Sunday start (0 = Sunday, 6 = Saturday)
    first_day_weekday = (first_day_weekday + 1) % 7
    
    # Calculate the start of the calendar (first Sunday)
    calendar_start = first_day - timedelta(days=first_day_weekday)
    
    # Get facility availability for the month
    availability_entries = FacilityAvailability.get_availability_for_month(year, month)
    
    # Get all bookings for the current month
    month_start = first_day.date()
    month_end = last_day.date()
    bookings = Booking.objects.filter(
        start_date__lte=month_end,
        end_date__gte=month_start
    )
    
    # Create calendar weeks
    calendar_weeks = []
    current_date = calendar_start
    
    for week in range(6):  # 6 weeks to ensure we cover the entire month
        week_days = []
        for day in range(7):
            if current_date.month == month:
                day_date = current_date.date()
                
                # Get availability entries for this day
                day_availability = availability_entries.filter(date=day_date)
                
                # Get bookings for this day
                day_bookings = bookings.filter(
                    start_date__lte=day_date,
                    end_date__gte=day_date
                )
                
                week_days.append({
                    'date': current_date,
                    'is_today': current_date.date() == timezone.now().date(),
                    'is_other_month': False,
                    'availability_entries': day_availability,
                    'booking_count': day_bookings.count(),
                    'is_facility_closed': FacilityAvailability.is_facility_closed(day_date),
                })
            else:
                week_days.append({
                    'date': current_date,
                    'is_today': False,
                    'is_other_month': True,
                    'availability_entries': [],
                    'booking_count': 0,
                    'is_facility_closed': False,
                })
            current_date += timedelta(days=1)
        calendar_weeks.append(week_days)
    
    context.update({
        'year': year,
        'month': month,
        'calendar_weeks': calendar_weeks,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'availability_entries': availability_entries,
    })
    return context

@user_passes_test(is_staff)
def delete_availability_entry(request, entry_id):
    """Delete a facility availability entry"""
    if request.method == 'POST':
        entry = get_object_or_404(FacilityAvailability, id=entry_id)
        entry.delete()
        
        # Redirect back to the same month/year
        year = int(request.GET.get('year', timezone.now().year))
        month = int(request.GET.get('month', timezone.now().month))
        from django.urls import reverse
        return redirect(f"{reverse('staff_calendar')}?year={year}&month={month}")
    return redirect('staff_calendar')
