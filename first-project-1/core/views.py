from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
import time
import csv
from django.core.mail import send_mail
from django.conf import settings

from .models import Owner, Dog, Kennel, Booking, DailyLog, Payment, StaffNote, FacilityAvailability

def is_staff(user):
    return user.is_staff or user.is_superuser

def is_owner(user):
    """Check if user is an owner (not staff)"""
    return not user.is_staff and not user.is_superuser

def home(request):
    """Homepage view - redirect to appropriate dashboard if logged in, otherwise show landing page"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff_dashboard')
        else:
            return redirect('owner_dashboard')
    
    return render(request, 'core/home.html')

def health_check(request):
    """Simple health check endpoint for Railway"""
    from django.http import JsonResponse
    return JsonResponse({
        'status': 'healthy',
        'message': 'Dog Boarding System is running',
        'timestamp': time.time()
    })

def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, "✅ You have been successfully logged out!")
    return redirect('home')

def debug_database(request):
    """Debug view to inspect database contents"""
    from django.contrib.auth.models import User
    from .models import Kennel
    
    try:
        user_count = User.objects.count()
        kennel_count = Kennel.objects.count()
        admin_exists = User.objects.filter(username='admin').exists()
        
        users = list(User.objects.all()[:10].values('username', 'email', 'is_staff', 'is_superuser'))
        kennels = list(Kennel.objects.all()[:10].values('name', 'size', 'is_available'))
        
        context = {
            'user_count': user_count,
            'kennel_count': kennel_count,
            'admin_exists': admin_exists,
            'users': users,
            'kennels': kennels,
        }
        
        return render(request, 'core/debug_database.html', context)
        
    except Exception as e:
        context = {
            'error': str(e),
            'user_count': 0,
            'kennel_count': 0,
            'admin_exists': False,
            'users': [],
            'kennels': [],
        }
        return render(request, 'core/debug_database.html', context)

def fix_session_table(request):
    """Database maintenance tool for staff only"""
    from django.core.management import call_command
    from django.contrib.auth.models import User
    from django.contrib.auth.decorators import user_passes_test
    
    # Check if user is staff
    if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
        from django.shortcuts import redirect
        return redirect('staff_login')
    
    if request.method == 'POST':
        try:
            # Run all Django migrations to create all tables
            call_command('migrate')
            
            # Create admin user if it doesn't exist
            if not User.objects.filter(username='admin').exists():
                User.objects.create_user(
                    username='admin',
                    email='admin@dogboarding.com',
                    password='admin123456',
                    first_name='Admin',
                    last_name='User',
                    is_staff=True,
                    is_superuser=True
                )
            
            # Create sample kennels if they don't exist
            from .models import Kennel
            kennel_sizes = [
                ('Small Kennel A', 'small', 'Cozy kennel for small dogs'),
                ('Small Kennel B', 'small', 'Cozy kennel for small dogs'),
                ('Medium Kennel A', 'medium', 'Comfortable kennel for medium dogs'),
                ('Medium Kennel B', 'medium', 'Comfortable kennel for medium dogs'),
                ('Large Kennel A', 'large', 'Spacious kennel for large dogs'),
                ('Large Kennel B', 'large', 'Spacious kennel for large dogs'),
            ]
            
            for name, size, description in kennel_sizes:
                Kennel.objects.get_or_create(
                    name=name,
                    defaults={
                        'size': size,
                        'description': description
                    }
                )
            
            messages.success(request, "✅ Database maintenance completed successfully!")
            messages.success(request, "🔑 Admin user: admin/admin123456")
            messages.success(request, "🏠 6 kennels created for bookings")
            return redirect('staff_dashboard')
            
        except Exception as e:
            messages.error(request, f"❌ Error during database maintenance: {str(e)}")
    
    return render(request, 'core/staff_fix_database.html')

def emergency_fix_database(request):
    """Emergency database fix - no authentication required"""
    from django.core.management import call_command
    from django.contrib.auth.models import User
    
    if request.method == 'POST':
        try:
            # Run all Django migrations to create all tables
            call_command('migrate')
            
            # Create admin user if it doesn't exist
            if not User.objects.filter(username='admin').exists():
                User.objects.create_user(
                    username='admin',
                    email='admin@dogboarding.com',
                    password='admin123456',
                    first_name='Admin',
                    last_name='User',
                    is_staff=True,
                    is_superuser=True
                )
            
            # Create sample kennels if they don't exist
            from .models import Kennel
            kennel_sizes = [
                ('Small Kennel A', 'small', 'Cozy kennel for small dogs'),
                ('Small Kennel B', 'small', 'Cozy kennel for small dogs'),
                ('Medium Kennel A', 'medium', 'Comfortable kennel for medium dogs'),
                ('Medium Kennel B', 'medium', 'Comfortable kennel for medium dogs'),
                ('Large Kennel A', 'large', 'Spacious kennel for large dogs'),
                ('Large Kennel B', 'large', 'Spacious kennel for large dogs'),
            ]
            
            for name, size, description in kennel_sizes:
                Kennel.objects.get_or_create(
                    name=name,
                    defaults={
                        'size': size,
                        'description': description
                    }
                )
            
            messages.success(request, "✅ Emergency database fix completed successfully!")
            messages.success(request, "🔑 Admin user: admin/admin123456")
            messages.success(request, "🏠 6 kennels created for bookings")
            messages.success(request, "🚀 You can now login at /staff/login/")
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f"❌ Error during emergency database fix: {str(e)}")
    
    return render(request, 'core/emergency_fix.html')

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

def create_admin_user_simple(request):
    """Create a simple admin user for testing"""
    try:
        from django.contrib.auth.models import User
        
        # Create admin user if it doesn't exist
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
            return HttpResponse(f"✅ Admin user created!<br>Username: admin<br>Password: admin123456<br><br><a href='/staff/login/'>Go to Staff Login</a>")
        else:
            return HttpResponse(f"✅ Admin user already exists!<br>Username: admin<br>Password: admin123456<br><br><a href='/staff/login/'>Go to Staff Login</a>")
            
    except Exception as e:
        return HttpResponse(f"❌ Error creating admin user: {str(e)}")

def setup_database(request):
    """Simple view to run database setup"""
    from django.db import connection
    from django.contrib.auth.hashers import make_password
    from django.utils import timezone
    
    if request.method == 'POST':
        try:
            # Step 1: Test database connection
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                messages.success(request, "✅ Database connection successful!")
            except Exception as db_error:
                messages.error(request, f"❌ Database connection failed: {str(db_error)}")
                return render(request, 'core/setup_database.html')
            
            # Step 2: Create basic tables using raw SQL
            try:
                messages.info(request, "📦 Creating database tables...")
                
                with connection.cursor() as cursor:
                    # Create django_migrations table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS django_migrations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            app VARCHAR(255) NOT NULL,
                            name VARCHAR(255) NOT NULL,
                            applied DATETIME(6) NOT NULL
                        )
                    """)
                    
                    # Create django_session table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS django_session (
                            session_key VARCHAR(40) PRIMARY KEY,
                            session_data TEXT NOT NULL,
                            expire_date DATETIME(6) NOT NULL
                        )
                    """)
                    
                    # Create django_content_type table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS django_content_type (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            app_label VARCHAR(100) NOT NULL,
                            model VARCHAR(100) NOT NULL,
                            UNIQUE(app_label, model)
                        )
                    """)
                    
                    # Create django_admin_log table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS django_admin_log (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            action_time DATETIME(6) NOT NULL,
                            object_id TEXT,
                            object_repr VARCHAR(200) NOT NULL,
                            action_flag SMALLINT UNSIGNED NOT NULL,
                            change_message TEXT NOT NULL,
                            content_type_id INTEGER,
                            user_id INTEGER NOT NULL,
                            FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
                            FOREIGN KEY (user_id) REFERENCES auth_user (id)
                        )
                    """)
                    
                    # Create auth_user table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS auth_user (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            password VARCHAR(128) NOT NULL,
                            last_login DATETIME(6),
                            is_superuser BOOLEAN NOT NULL,
                            username VARCHAR(150) UNIQUE NOT NULL,
                            first_name VARCHAR(150) NOT NULL,
                            last_name VARCHAR(150) NOT NULL,
                            email VARCHAR(254) NOT NULL,
                            is_staff BOOLEAN NOT NULL,
                            is_active BOOLEAN NOT NULL,
                            date_joined DATETIME(6) NOT NULL
                        )
                    """)
                    
                    # Create core_owner table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS core_owner (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL UNIQUE,
                            phone VARCHAR(20) NOT NULL,
                            address TEXT NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES auth_user (id)
                        )
                    """)
                    
                    # Create core_kennel table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS core_kennel (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name VARCHAR(100) NOT NULL,
                            description TEXT NOT NULL,
                            size VARCHAR(20) NOT NULL,
                            is_available BOOLEAN NOT NULL DEFAULT 1
                        )
                    """)
                    
                    # Create core_dog table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS core_dog (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name VARCHAR(100) NOT NULL,
                            breed VARCHAR(100) NOT NULL,
                            age INTEGER NOT NULL,
                            size VARCHAR(20) NOT NULL,
                            notes TEXT,
                            photo VARCHAR(100),
                            owner_id INTEGER NOT NULL,
                            FOREIGN KEY (owner_id) REFERENCES core_owner (id)
                        )
                    """)
                    
                    # Create core_booking table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS core_booking (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            dog_id INTEGER NOT NULL,
                            start_date DATE NOT NULL,
                            end_date DATE NOT NULL,
                            status VARCHAR(20) NOT NULL DEFAULT 'pending',
                            notes TEXT,
                            total_amount DECIMAL(10,2),
                            price_per_night DECIMAL(10,2),
                            kennel_id INTEGER,
                            created_at DATETIME(6) NOT NULL,
                            FOREIGN KEY (dog_id) REFERENCES core_dog (id),
                            FOREIGN KEY (kennel_id) REFERENCES core_kennel (id)
                        )
                    """)
                    
                    # Create core_payment table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS core_payment (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            booking_id INTEGER NOT NULL UNIQUE,
                            amount DECIMAL(10,2) NOT NULL,
                            status VARCHAR(20) NOT NULL DEFAULT 'pending',
                            payment_method VARCHAR(20),
                            paid_date DATETIME(6),
                            notes TEXT,
                            created_at DATETIME(6) NOT NULL,
                            FOREIGN KEY (booking_id) REFERENCES core_booking (id)
                        )
                    """)
                    
                    # Create core_dailylog table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS core_dailylog (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            booking_id INTEGER NOT NULL,
                            date DATE NOT NULL,
                            feeding TEXT,
                            medication TEXT,
                            exercise TEXT,
                            notes TEXT,
                            FOREIGN KEY (booking_id) REFERENCES core_booking (id)
                        )
                    """)
                    
                    # Create core_staffnote table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS core_staffnote (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            booking_id INTEGER NOT NULL,
                            staff_member_id INTEGER NOT NULL,
                            note TEXT NOT NULL,
                            picture VARCHAR(100),
                            created_at DATETIME(6) NOT NULL,
                            FOREIGN KEY (booking_id) REFERENCES core_booking (id),
                            FOREIGN KEY (staff_member_id) REFERENCES auth_user (id)
                        )
                    """)
                    
                    # Create core_facilityavailability table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS core_facilityavailability (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date DATE NOT NULL,
                            type VARCHAR(20) NOT NULL,
                            title VARCHAR(100) NOT NULL,
                            description TEXT,
                            created_by_id INTEGER NOT NULL,
                            created_at DATETIME(6) NOT NULL,
                            FOREIGN KEY (created_by_id) REFERENCES auth_user (id)
                        )
                    """)
                
                messages.success(request, "✅ Database tables created!")
                    
            except Exception as table_error:
                messages.error(request, f"❌ Table creation failed: {str(table_error)}")
                return render(request, 'core/setup_database.html')
            
            # Step 3: Create admin user using Django ORM
            try:
                messages.info(request, "👤 Creating admin user...")
                
                from django.contrib.auth.models import User
                
                # Check if admin user exists
                if not User.objects.filter(username='admin').exists():
                    # Create admin user using Django's ORM
                    admin_user = User.objects.create_user(
                        username='admin',
                        email='admin@dogboarding.com',
                        password='admin123456',
                        first_name='Admin',
                        last_name='User',
                        is_staff=True,
                        is_superuser=True
                    )
                    
                    messages.success(request, "✅ Admin user created: admin/admin123456")
                else:
                    messages.info(request, "ℹ️ Admin user already exists")
                
            except Exception as user_error:
                messages.error(request, f"❌ User creation failed: {str(user_error)}")
                return render(request, 'core/setup_database.html')
            
            # Step 4: Create sample kennels using Django ORM
            try:
                messages.info(request, "🏠 Creating sample kennels...")
                
                from .models import Kennel
                
                # Check if kennels exist
                if not Kennel.objects.exists():
                    # Create sample kennels
                    kennel_data = [
                        {'name': 'Small Kennel A', 'description': 'Cozy kennel for small dogs', 'size': 'small'},
                        {'name': 'Small Kennel B', 'description': 'Cozy kennel for small dogs', 'size': 'small'},
                        {'name': 'Medium Kennel A', 'description': 'Comfortable kennel for medium dogs', 'size': 'medium'},
                        {'name': 'Medium Kennel B', 'description': 'Comfortable kennel for medium dogs', 'size': 'medium'},
                        {'name': 'Large Kennel A', 'description': 'Spacious kennel for large dogs', 'size': 'large'},
                        {'name': 'Large Kennel B', 'description': 'Spacious kennel for large dogs', 'size': 'large'},
                    ]
                    
                    for kennel_info in kennel_data:
                        Kennel.objects.create(**kennel_info)
                    
                    messages.success(request, "✅ Sample kennels created!")
                else:
                    messages.info(request, "ℹ️ Kennels already exist")
                
            except Exception as kennel_error:
                messages.error(request, f"❌ Kennel creation failed: {str(kennel_error)}")
                return render(request, 'core/setup_database.html')
            
            messages.success(request, "🎉 Database setup completed successfully!")
            messages.success(request, "📝 You can now login as admin (admin/admin123456)")
            return redirect('setup_database')
            
        except Exception as e:
            messages.error(request, f"❌ Unexpected error: {str(e)}")
            messages.error(request, "💡 Please check Railway logs for more details")
    
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
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': '(555) 123-4567',
            'pattern': '[\\(]?[0-9]{3}[\\)]?[\\s-]?[0-9]{3}[\\s-]?[0-9]{4}',
            'title': 'Please enter a valid phone number: (555) 123-4567'
        })
    )

    class Meta:
        model = Owner
        fields = ['address']

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
    """Owner login view"""
    import logging
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        logger.info("Login attempt received")
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            logger.info("Form is valid, attempting authentication")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            logger.info(f"Authentication result for {username}: {user is not None}")
            
            if user is not None:
                try:
                    owner = Owner.objects.get(user=user)
                    logger.info(f"Owner found: {owner}")
                    login(request, user)
                    logger.info("User logged in successfully")
                    return redirect('owner_dashboard')
                except Owner.DoesNotExist:
                    logger.error(f"User {username} exists but no Owner record found")
                    form.add_error(None, "This account is not set up as a dog owner. Please register as an owner first.")
            else:
                logger.error(f"Authentication failed for username: {username}")
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        logger.info("Rendering login form")
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

def create_test_owner(request):
    """Create a test owner account for testing"""
    from django.contrib.auth.models import User
    
    if request.method == 'POST':
        try:
            # Create test user if it doesn't exist
            if not User.objects.filter(username='testowner').exists():
                test_user = User.objects.create_user(
                    username='testowner',
                    email='test@example.com',
                    password='test123456',
                    first_name='Test',
                    last_name='Owner'
                )
                
                # Create Owner record
                Owner.objects.create(
                    user=test_user,
                    phone='555-1234',
                    address='123 Test Street'
                )
                messages.success(request, "✅ Test owner created: testowner/test123456")
            else:
                messages.info(request, "ℹ️ Test owner already exists: testowner/test123456")
            
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f"❌ Error creating test owner: {str(e)}")
    
    return render(request, 'core/create_test_owner.html')

def test_admin_fix(request):
    """Test the admin fix by creating an owner and checking the relationship"""
    from django.contrib.auth.models import User
    
    try:
        # Create a test owner if it doesn't exist
        if not User.objects.filter(username='admintest').exists():
            test_user = User.objects.create_user(
                username='admintest',
                email='admintest@example.com',
                password='admintest123',
                first_name='Admin',
                last_name='Test'
            )
            
            owner = Owner.objects.create(
                user=test_user,
                phone='555-9999',
                address='999 Test Street'
            )
            
            # Test the dogs relationship
            dog_count = owner.dogs.count()
            
            return render(request, 'core/test_admin_fix.html', {
                'success': True,
                'owner': owner,
                'dog_count': dog_count,
                'message': f"✅ Admin fix working! Owner has {dog_count} dogs."
            })
        else:
            owner = Owner.objects.get(user__username='admintest')
            dog_count = owner.dogs.count()
            
            return render(request, 'core/test_admin_fix.html', {
                'success': True,
                'owner': owner,
                'dog_count': dog_count,
                'message': f"✅ Admin fix working! Owner has {dog_count} dogs."
            })
            
    except Exception as e:
        return render(request, 'core/test_admin_fix.html', {
            'success': False,
            'error': str(e)
        })

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
@user_passes_test(is_owner)
def owner_dashboard(request):
    """Full dashboard with database access and error handling"""
    try:
        # Get owner
        try:
            owner = request.user.owner
        except Owner.DoesNotExist:
            return redirect('register_owner')
        
        # Get dogs with safe field access
        try:
            dogs = Dog.objects.filter(owner=owner)
        except Exception as e:
            print(f"Error fetching dogs: {e}")
            dogs = []
        
        context = {
            'owner': owner,
            'dogs': dogs,
        }
        return render(request, 'core/dashboard_minimal.html', context)
    except Exception as e:
        return HttpResponse(f"Dashboard Error: {str(e)}")

@login_required
@user_passes_test(is_owner)
def add_dog(request):
    """Add dog with improved error handling"""
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('login_owner')
        
        # Try to get owner, redirect to create owner if not found
        try:
            owner = get_object_or_404(Owner, user=request.user)
        except:
            return redirect('register_owner')
        
        if request.method == 'POST':
            try:
                form = DogForm(request.POST, request.FILES)
                if form.is_valid():
                    dog = form.save(commit=False)
                    dog.owner = owner
                    dog.save()
                    # Comment out base64 saving for now to avoid errors
                    # if request.FILES.get('photo'):
                    #     dog.save_photo_as_base64(request.FILES['photo'])
                    return redirect('owner_dashboard')
                else:
                    return render(request, 'core/add_dog.html', {'form': form})
            except Exception as e:
                return HttpResponse(f"Error saving dog: {str(e)}")
        else:
            try:
                form = DogForm()
                return render(request, 'core/add_dog.html', {'form': form})
            except Exception as e:
                return HttpResponse(f"Error loading dog form: {str(e)}")
        
    except Exception as e:
        return HttpResponse(f"Add dog error: {str(e)}")

@login_required
@user_passes_test(is_owner)
def edit_dog(request, dog_id):
    """Edit dog with improved error handling"""
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('login_owner')
        
        # Try to get owner, redirect to create owner if not found
        try:
            owner = get_object_or_404(Owner, user=request.user)
        except:
            return redirect('register_owner')
        
        # Try to get dog, handle 404 gracefully
        try:
            dog = get_object_or_404(Dog, id=dog_id, owner=owner)
        except:
            return HttpResponse(f"Dog with ID {dog_id} not found or you don't have permission to edit it.")
        
        if request.method == 'POST':
            try:
                form = DogForm(request.POST, request.FILES, instance=dog)
                if form.is_valid():
                    dog = form.save()
                    # Comment out base64 saving for now to avoid errors
                    # dog.save_photo_as_base64()
                    return redirect('owner_dashboard')
                else:
                    return render(request, 'core/edit_dog.html', {'form': form, 'dog': dog})
            except Exception as e:
                return HttpResponse(f"Error saving dog: {str(e)}")
        else:
            try:
                form = DogForm(instance=dog)
                return render(request, 'core/edit_dog.html', {'form': form, 'dog': dog})
            except Exception as e:
                return HttpResponse(f"Error loading dog form: {str(e)}")
        
    except Exception as e:
        return HttpResponse(f"Edit dog error: {str(e)}")

@login_required
@user_passes_test(is_owner)
def delete_dog(request, dog_id):
    owner = get_object_or_404(Owner, user=request.user)
    dog = get_object_or_404(Dog, id=dog_id, owner=owner)
    if request.method == 'POST':
        dog.delete()
        return redirect('owner_dashboard')
    return render(request, 'core/delete_dog.html', {'dog': dog})

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['dog', 'start_date', 'end_date', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'mm/dd/yyyy',
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'mm/dd/yyyy',
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Any special instructions or notes...'
            }),
        }

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            # Get dogs with minimal field access
            dogs = Dog.objects.filter(owner=owner).values('id', 'name', 'breed', 'size')
            self.fields['dog'].queryset = Dog.objects.filter(owner=owner)
            self.fields['dog'].widget.attrs.update({'class': 'form-control'})
        except Exception as e:
            print(f"Error initializing booking form: {e}")
            self.fields['dog'].queryset = Dog.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        try:
            dog = cleaned_data.get('dog')
            kennel = None  # Simplified for now
            
            if dog and kennel:
                size_compatibility = {
                    'small': ['small', 'medium', 'large'],
                    'medium': ['medium', 'large'],
                    'large': ['large']
                }
                if kennel.size not in size_compatibility.get(dog.size, ['large']):
                    raise ValidationError(f"A {dog.get_size_display()} dog cannot be placed in a {kennel.get_size_display()} kennel.")
        except Exception as e:
            print(f"Booking form validation error: {e}")
        return cleaned_data

@login_required
@user_passes_test(is_owner)
def booking_calendar(request):
    """Booking calendar with improved error handling"""
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('login_owner')
        
        # Try to get owner, redirect to create owner if not found
        try:
            owner = get_object_or_404(Owner, user=request.user)
        except:
            return redirect('register_owner')
        
        # Get year and month from URL parameters, default to current month
        try:
            year = int(request.GET.get('year', timezone.now().year))
            month = int(request.GET.get('month', timezone.now().month))
        except (ValueError, TypeError):
            year = timezone.now().year
            month = timezone.now().month
        
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
        try:
            first_day = datetime(year, month, 1)
            if month == 12:
                last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                last_day = datetime(year, month + 1, 1) - timedelta(days=1)
        except ValueError as e:
            return HttpResponse(f"Invalid date calculation: {str(e)}")
        
        # Get the day of the week for the first day (0 = Monday, 6 = Sunday)
        first_day_weekday = first_day.weekday()
        
        # Adjust for Sunday start (0 = Sunday, 6 = Saturday)
        first_day_weekday = (first_day_weekday + 1) % 7
        
        # Calculate the start of the calendar (first Sunday)
        calendar_start = first_day - timedelta(days=first_day_weekday)
        
        # Get all kennels for availability calculation
        try:
            kennels = Kennel.objects.all()
        except Exception as e:
            return HttpResponse(f"Error loading kennels: {str(e)}")
        
        # Get all bookings for the current month
        try:
            month_start = first_day.date()
            month_end = last_day.date()
            bookings = Booking.objects.filter(
                start_date__lte=month_end,
                end_date__gte=month_start
            ).exclude(status='cancelled')
        except Exception as e:
            return HttpResponse(f"Error loading bookings: {str(e)}")
        
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
                    
                    try:
                        for kennel in kennels:
                            if kennel.is_available_for_dates(day_date, day_date):
                                available_kennels.append(kennel)
                    except Exception as e:
                        # If kennel availability check fails, assume all available
                        available_kennels = list(kennels)
                    
                    # Calculate availability percentage
                    availability_percentage = (len(available_kennels) / total_kennels * 100) if total_kennels > 0 else 0
                    
                    # Check if there are any bookings for this day
                    try:
                        day_bookings = bookings.filter(
                            start_date__lte=day_date,
                            end_date__gte=day_date
                        )
                        has_booking = day_bookings.exists()
                        booking_count = day_bookings.count()
                        
                        # Get booking details for display
                        booking_details = []
                        for booking in day_bookings:
                            booking_details.append({
                                'dog_name': booking.dog.name,
                                'owner_name': f"{booking.dog.owner.user.first_name} {booking.dog.owner.user.last_name}".strip(),
                                'kennel_name': booking.kennel.name if booking.kennel else 'No kennel assigned'
                            })
                    except Exception as e:
                        has_booking = False
                        booking_count = 0
                        booking_details = []
                    
                    week_days.append({
                        'date': current_date,
                        'is_today': current_date.date() == timezone.now().date(),
                        'is_other_month': False,
                        'has_booking': has_booking,
                        'booking_count': booking_count,
                        'booking_details': booking_details,
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
                        'booking_details': [],
                        'available_kennels': 0,
                        'total_kennels': 0,
                        'availability_percentage': 0,
                        'availability_status': 'none'
                    })
                current_date += timedelta(days=1)
            calendar_weeks.append(week_days)
        
        context = {
            'calendar_weeks': calendar_weeks,
            'year': year,
            'month': month,
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year,
            'month_name': first_day.strftime('%m/%Y'),
            'year_name': first_day.strftime('%Y'),
        }
        
        return render(request, 'core/booking_calendar.html', context)
    except Exception as e:
        return HttpResponse(f"Booking calendar error: {str(e)}")

@login_required
@user_passes_test(is_owner)
def create_booking(request):
    """Create booking with improved error handling"""
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('login_owner')
        
        # Try to get owner, redirect to create owner if not found
        try:
            owner = get_object_or_404(Owner, user=request.user)
        except:
            return redirect('register_owner')
        
        if request.method == 'POST':
            form = BookingForm(owner, request.POST)
            if form.is_valid():
                try:
                    booking = form.save(commit=False)
                    booking.dog = form.cleaned_data['dog']
                    booking.save()
                    return redirect('booking_list')
                except Exception as e:
                    return HttpResponse(f"Booking creation error: {str(e)}")
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
        
        # Get all kennels for the dropdown
        all_kennels = Kennel.objects.all().order_by('name')
        
        # Get available kennels based on selected dates and dog size
        available_kennels = []
        if request.GET.get('start_date') and request.GET.get('end_date'):
            try:
                start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
                end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
                
                # Get all kennels that are available for the selected dates
                for kennel in all_kennels:
                    if kennel.is_available_for_dates(start_date, end_date):
                        available_kennels.append(kennel)
            except ValueError:
                pass
        
        return render(request, 'core/create_booking.html', {
            'form': form,
            'available_kennels': available_kennels,
            'all_kennels': all_kennels
        })
        
    except Exception as e:
        return HttpResponse(f"Create booking error: {str(e)}")

@login_required
@user_passes_test(is_owner)
def get_available_kennels(request):
    """Get available kennels for selected dates via AJAX"""
    try:
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        dog_size = request.GET.get('dog_size', 'medium')
        
        if not start_date_str or not end_date_str:
            return JsonResponse({'kennels': [], 'message': 'Please select both start and end dates'})
        
        # Convert dates from mm/dd/yyyy to YYYY-MM-DD
        try:
            start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date()
            end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date()
        except ValueError:
            return JsonResponse({'kennels': [], 'message': 'Invalid date format'})
        
        # Get all kennels
        all_kennels = Kennel.objects.all().order_by('name')
        available_kennels = []
        
        # Size compatibility mapping
        size_compatibility = {
            'small': ['small', 'medium', 'large'],
            'medium': ['medium', 'large'],
            'large': ['large']
        }
        
        for kennel in all_kennels:
            # Check if kennel is available for the dates
            if kennel.is_available_for_dates(start_date, end_date):
                # Check if kennel size is compatible with dog size
                if kennel.size in size_compatibility.get(dog_size, ['large']):
                    available_kennels.append({
                        'id': kennel.id,
                        'name': kennel.name,
                        'size': kennel.get_size_display(),
                        'description': kennel.description
                    })
        

        return JsonResponse({
            'kennels': available_kennels,
            'message': f'Found {len(available_kennels)} available kennels for your dates'
        })
        
    except Exception as e:
        return JsonResponse({'kennels': [], 'message': f'Error: {str(e)}'})

@login_required
@user_passes_test(is_owner)
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
@user_passes_test(is_owner)
def cancel_booking(request, booking_id):
    owner = get_object_or_404(Owner, user=request.user)
    booking = get_object_or_404(Booking, id=booking_id, dog__owner=owner)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        return redirect('booking_list')
    
    return render(request, 'core/cancel_booking.html', {'booking': booking})

def test_staff_status(request):
    """Test view to check if user is staff"""
    try:
        if request.user.is_authenticated:
            is_staff_user = is_staff(request.user)
            return HttpResponse(f"""
            <h2>Staff Status Test</h2>
            <p>Username: {request.user.username}</p>
            <p>Is Staff: {request.user.is_staff}</p>
            <p>Is Superuser: {request.user.is_superuser}</p>
            <p>Is Staff (function): {is_staff_user}</p>
            <p>Is Authenticated: {request.user.is_authenticated}</p>
            <br>
            <a href="/staff/dashboard/">Try Staff Dashboard</a>
            """)
        else:
            return HttpResponse("Not authenticated. Please <a href='/staff/login/'>login</a> first.")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

@user_passes_test(is_staff)
def staff_dashboard(request):
    """Staff dashboard with error handling"""
    try:
        # Get filter parameters
        filter_type = request.GET.get('filter_type', 'month')  # 'month', 'year', 'all_time'
        filter_month = request.GET.get('month', timezone.now().month)
        filter_year = request.GET.get('year', timezone.now().year)
        
        try:
            filter_month = int(filter_month)
            filter_year = int(filter_year)
        except (ValueError, TypeError):
            filter_month = timezone.now().month
            filter_year = timezone.now().year
        
        # Calculate date range for filtering based on filter type
        if filter_type == 'all_time':
            # No date filtering - show all time data
            start_date = None
            end_date = None
            bookings = Booking.objects.all().order_by('start_date')
            period_payments = Payment.objects.all()
        elif filter_type == 'year':
            # Filter by specific year
            start_date = datetime(filter_year, 1, 1).date()
            end_date = datetime(filter_year, 12, 31).date()
            bookings = Booking.objects.filter(
                start_date__lte=end_date,
                end_date__gte=start_date
            ).order_by('start_date')
            period_payments = Payment.objects.filter(
                booking__start_date__lte=end_date,
                booking__end_date__gte=start_date
            )
        else:
            # Default: filter by specific month
            if filter_month == 12:
                next_month = 1
                next_year = filter_year + 1
            else:
                next_month = filter_month + 1
                next_year = filter_year
            
            start_date = datetime(filter_year, filter_month, 1).date()
            end_date = datetime(next_year, next_month, 1).date() - timedelta(days=1)
            
            bookings = Booking.objects.filter(
                start_date__lte=end_date,
                end_date__gte=start_date
            ).order_by('start_date')
            period_payments = Payment.objects.filter(
                booking__start_date__lte=end_date,
                booking__end_date__gte=start_date
            )
        
        # Get upcoming bookings (next 7 days)
        today = timezone.now().date()
        upcoming_bookings = Booking.objects.filter(
            start_date__gte=today,
            status='confirmed'
        ).order_by('start_date')[:10]
        
        # Get pending bookings for the filtered period
        pending_bookings = bookings.filter(status='pending')
        
        # Get cancelled bookings for the filtered period
        cancelled_bookings = bookings.filter(status='cancelled')
        
        # Get kennel assignments
        kennels = Kennel.objects.all()
        
        # Calculate payment statistics
        # Total revenue for the filtered period
        total_revenue = sum(payment.amount for payment in period_payments.filter(status='paid'))
        
        # Pending payments filtered by the selected period
        if filter_type == 'all_time':
            # Show all pending payments for all time
            pending_payments = sum(payment.amount for payment in Payment.objects.filter(status='pending'))
        elif filter_type == 'year':
            # Filter pending payments by the selected year
            year_start = datetime(filter_year, 1, 1).date()
            year_end = datetime(filter_year, 12, 31).date()
            pending_payments = sum(
                payment.amount for payment in Payment.objects.filter(
                    status='pending',
                    booking__start_date__lte=year_end,
                    booking__end_date__gte=year_start
                )
            )
        else:
            # Filter pending payments by the selected month
            if filter_month == 12:
                next_month = 1
                next_year = filter_year + 1
            else:
                next_month = filter_month + 1
                next_year = filter_year
            
            month_start = datetime(filter_year, filter_month, 1).date()
            month_end = datetime(next_year, next_month, 1).date() - timedelta(days=1)
            
            pending_payments = sum(
                payment.amount for payment in Payment.objects.filter(
                    status='pending',
                    booking__start_date__lte=month_end,
                    booking__end_date__gte=month_start
                )
            )
        
        # Get all bookings for total count (not filtered by period)
        all_bookings = Booking.objects.all()
        
        # Generate year options for the dropdown
        current_year = timezone.now().year
        year_options = range(current_year - 2, current_year + 3)  # 2 years back, 2 years forward
        
        context = {
            'upcoming_bookings': upcoming_bookings,
            'pending_bookings': pending_bookings,
            'cancelled_bookings': cancelled_bookings,
            'kennels': kennels,
            'total_bookings': all_bookings.count(),
            'filtered_bookings': bookings.count(),
            'total_pending': pending_bookings.count(),
            'total_cancelled': cancelled_bookings.count(),
            'total_revenue': total_revenue,
            'pending_payments': pending_payments,
            'filter_type': filter_type,
            'filter_month': filter_month,
            'filter_year': filter_year,
            'start_date': start_date,
            'end_date': end_date,
            'year_options': year_options,
            'month_name': datetime(filter_year, filter_month, 1).strftime('%m/%Y') if filter_type == 'month' else f'{filter_year}' if filter_type == 'year' else 'All Time',
        }
        return render(request, 'core/staff_dashboard.html', context)
    except Exception as e:
        return HttpResponse(f"Staff dashboard error: {str(e)}")

@user_passes_test(is_staff)
def staff_booking_list(request):
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    filter_type = request.GET.get('filter_type', 'all_time')  # 'month', 'year', 'all_time'
    filter_month = request.GET.get('month', timezone.now().month)
    filter_year = request.GET.get('year', timezone.now().year)
    kennel_size_filter = request.GET.get('kennel_size', 'all')
    
    try:
        filter_month = int(filter_month)
        filter_year = int(filter_year)
    except (ValueError, TypeError):
        filter_month = timezone.now().month
        filter_year = timezone.now().year
    
    # Get all bookings
    bookings = Booking.objects.all().order_by('-created_at')
    
    # Apply status filter
    if status_filter != 'all':
        bookings = bookings.filter(status=status_filter)
    
    # Apply date filter
    if filter_type == 'month':
        # Filter by specific month
        if filter_month == 12:
            next_month = 1
            next_year = filter_year + 1
        else:
            next_month = filter_month + 1
            next_year = filter_year
        
        start_date = datetime(filter_year, filter_month, 1).date()
        end_date = datetime(next_year, next_month, 1).date() - timedelta(days=1)
        
        bookings = bookings.filter(
            start_date__lte=end_date,
            end_date__gte=start_date
        )
    elif filter_type == 'year':
        # Filter by specific year
        start_date = datetime(filter_year, 1, 1).date()
        end_date = datetime(filter_year, 12, 31).date()
        
        bookings = bookings.filter(
            start_date__lte=end_date,
            end_date__gte=start_date
        )
    # 'all_time' - no date filtering
    
    # Apply kennel size filter
    if kennel_size_filter != 'all':
        bookings = bookings.filter(kennel__size=kennel_size_filter)
    
    # Get all status choices for the filter dropdown
    status_choices = [('all', 'All Bookings')] + list(Booking.STATUS_CHOICES)
    
    # Get kennel size choices
    kennel_size_choices = [('all', 'All Sizes')] + list(Kennel.SIZE_CHOICES)
    
    # Generate year options for the dropdown
    current_year = timezone.now().year
    year_options = range(current_year - 2, current_year + 3)  # 2 years back, 2 years forward
    
    context = {
        'bookings': bookings,
        'status_choices': status_choices,
        'kennel_size_choices': kennel_size_choices,
        'current_filter': status_filter,
        'filter_type': filter_type,
        'filter_month': filter_month,
        'filter_year': filter_year,
        'kennel_size_filter': kennel_size_filter,
        'year_options': year_options,
        'month_name': datetime(filter_year, filter_month, 1).strftime('%m/%Y') if filter_type == 'month' else f'{filter_year}' if filter_type == 'year' else 'All Time',
    }
    return render(request, 'core/staff_booking_list.html', context)

@user_passes_test(is_staff)
def staff_booking_detail(request, booking_id):
    """Staff view to manage a specific booking"""
    try:
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
                    if kennel.is_available_for_dates(booking.start_date, booking.end_date, booking):
                        # Check size compatibility
                        size_compatibility = {
                            'small': ['small', 'medium', 'large'],
                            'medium': ['medium', 'large'],
                            'large': ['large']
                        }
                        if kennel.size in size_compatibility.get(booking.dog.size, ['large']):
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
        
        # Calculate nights
        nights = (booking.end_date - booking.start_date).days
        
        context = {
            'booking': booking,
            'available_kennels': available_kennels,
            'all_kennels': all_kennels,
            'staff_notes': staff_notes,
            'nights': nights,
            'owner_name': f"{booking.dog.owner.user.first_name} {booking.dog.owner.user.last_name}".strip() or booking.dog.owner.user.username,
        }
        
        return render(request, 'core/staff_booking_detail.html', context)
        
    except Exception as e:
        return HttpResponse(f"❌ Error loading booking: {str(e)}")

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
    period_filter = request.GET.get('period', 'all')  # New period filter
    
    kennels = Kennel.objects.all()
    
    # Apply size filter
    if size_filter != 'all':
        kennels = kennels.filter(size=size_filter)
    
    # Calculate date range for period filter
    today = timezone.now().date()
    if period_filter == 'week':
        start_date = today - timedelta(days=7)
        end_date = today + timedelta(days=7)
    elif period_filter == 'month':
        start_date = today - timedelta(days=30)
        end_date = today + timedelta(days=30)
    else:  # 'all' or default
        start_date = None
        end_date = None
    
    # Get bookings for each kennel and apply availability filter
    for kennel in kennels:
        booking_query = Booking.objects.filter(
            kennel=kennel,
            status__in=['confirmed', 'pending']
        )
        
        # Apply period filter if specified
        if start_date and end_date:
            booking_query = booking_query.filter(
                start_date__lte=end_date,
                end_date__gte=start_date
            )
        else:
            # Default to current bookings
            booking_query = booking_query.filter(
                start_date__lte=today,
                end_date__gte=today
            )
        
        kennel.current_bookings = booking_query
        kennel.period_bookings = booking_query.count()
    
    # Apply availability filter
    if availability_filter == 'available':
        kennels = [kennel for kennel in kennels if not kennel.current_bookings]
    elif availability_filter == 'occupied':
        kennels = [kennel for kennel in kennels if kennel.current_bookings]
    
    # Calculate meaningful statistics
    total_kennels = Kennel.objects.count()
    available_kennels = sum(1 for k in kennels if not k.current_bookings)
    occupied_kennels = sum(1 for k in kennels if k.current_bookings)
    total_bookings_period = sum(k.period_bookings for k in kennels)
    
    return render(request, 'core/staff_kennel_management.html', {
        'kennels': kennels,
        'form': form,
        'size_filter': size_filter,
        'availability_filter': availability_filter,
        'period_filter': period_filter,
        'size_choices': Kennel.SIZE_CHOICES,
        'total_kennels': total_kennels,
        'available_kennels': available_kennels,
        'occupied_kennels': occupied_kennels,
        'total_bookings_period': total_bookings_period,
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
            messages.success(request, f"Kennel '{kennel.name}' updated successfully!")
            return redirect('staff_kennel_management')
        else:
            messages.error(request, "Please provide a valid kennel name and size.")
    
    return render(request, 'core/edit_kennel.html', {
        'kennel': kennel
    })

def staff_login(request):
    """Staff login with improved error handling"""
    try:
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
                form.add_error(None, "Invalid username or password.")
        else:
            form = AuthenticationForm()
        return render(request, 'core/staff_login.html', {'form': form})
    except Exception as e:
        return HttpResponse(f"Staff login error: {str(e)}")

@user_passes_test(is_staff)
def staff_payment_list(request):
    """Staff view to manage all payments"""
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    filter_type = request.GET.get('filter_type', 'all_time')  # 'month', 'year', 'all_time'
    filter_month = request.GET.get('month', timezone.now().month)
    filter_year = request.GET.get('year', timezone.now().year)
    
    try:
        filter_month = int(filter_month)
        filter_year = int(filter_year)
    except (ValueError, TypeError):
        filter_month = timezone.now().month
        filter_year = timezone.now().year
    
    # Get all payments
    payments = Payment.objects.all().order_by('-created_at')
    
    # Apply status filter
    if status_filter != 'all':
        payments = payments.filter(status=status_filter)
    
    # Apply date filter
    if filter_type == 'month':
        # Filter by specific month
        if filter_month == 12:
            next_month = 1
            next_year = filter_year + 1
        else:
            next_month = filter_month + 1
            next_year = filter_year
        
        start_date = datetime(filter_year, filter_month, 1).date()
        end_date = datetime(next_year, next_month, 1).date() - timedelta(days=1)
        
        payments = payments.filter(
            booking__start_date__lte=end_date,
            booking__end_date__gte=start_date
        )
    elif filter_type == 'year':
        # Filter by specific year
        start_date = datetime(filter_year, 1, 1).date()
        end_date = datetime(filter_year, 12, 31).date()
        
        payments = payments.filter(
            booking__start_date__lte=end_date,
            booking__end_date__gte=start_date
        )
    # 'all_time' - no date filtering
    
    # Generate year options for the dropdown
    current_year = timezone.now().year
    year_options = range(current_year - 2, current_year + 3)  # 2 years back, 2 years forward
    
    context = {
        'payments': payments,
        'status_choices': [('all', 'All Payments')] + list(Payment.PAYMENT_STATUS_CHOICES),
        'current_filter': status_filter,
        'filter_type': filter_type,
        'filter_month': filter_month,
        'filter_year': filter_year,
        'year_options': year_options,
        'month_name': datetime(filter_year, filter_month, 1).strftime('%m/%Y') if filter_type == 'month' else f'{filter_year}' if filter_type == 'year' else 'All Time',
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
            # Allow empty string to clear the payment method
            payment.payment_method = payment_method if payment_method else ''
            payment.save()
            messages.success(request, "Payment method updated successfully!")
        
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
            
            # Add success message
            messages.success(request, f"Availability entry '{availability.title}' has been saved successfully!")
            
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
    ).exclude(status='cancelled')
    
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
                
                # Get booking details with dog names
                booking_details = []
                for booking in day_bookings:
                    owner_name = 'Unknown'
                    if booking.dog.owner and booking.dog.owner.user:
                        owner_name = booking.dog.owner.user.get_full_name() or booking.dog.owner.user.username
                    
                    booking_details.append({
                        'id': booking.id,
                        'dog_name': booking.dog.name,
                        'owner_name': owner_name,
                        'status': booking.status,
                        'total_amount': booking.total_amount
                    })
                
                week_days.append({
                    'date': current_date,
                    'is_today': current_date.date() == timezone.now().date(),
                    'is_other_month': False,
                    'availability_entries': day_availability,
                    'booking_count': day_bookings.count(),
                    'booking_details': booking_details,
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

def debug_app(request):
    """Debug endpoint to check app status"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check user authentication
    if request.user.is_authenticated:
        user_status = f"authenticated as {request.user.username}"
        try:
            owner = Owner.objects.get(user=request.user)
            owner_status = f"owner found: {owner}"
        except Owner.DoesNotExist:
            owner_status = "no owner record"
    else:
        user_status = "not authenticated"
        owner_status = "not found"
    
    import time
    return JsonResponse({
        'status': 'running',
        'database': db_status,
        'user': user_status,
        'owner': owner_status,
        'timestamp': time.time()
    })

def create_test_user_simple(request):
    """Create a simple test user for debugging"""
    try:
        from django.contrib.auth.models import User
        from django.contrib.auth.hashers import make_password
        
        # Create test user
        username = 'testuser'
        password = 'testpass123'
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
        else:
            user = User.objects.create_user(
                username=username,
                email='test@example.com',
                password=password,
                first_name='Test',
                last_name='User'
            )
        
        # Create owner record
        owner, created = Owner.objects.get_or_create(
            user=user,
            defaults={
                'phone': '555-1234',
                'address': '123 Test St'
            }
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Test user created: {username} / {password}',
            'user_id': user.id,
            'owner_id': owner.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def list_users(request):
    """Debug endpoint to list existing users"""
    from django.http import JsonResponse
    from django.contrib.auth.models import User
    
    try:
        users = []
        for user in User.objects.all():
            try:
                owner = Owner.objects.get(user=user)
                owner_status = "has owner record"
            except Owner.DoesNotExist:
                owner_status = "no owner record"
            
            users.append({
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'owner_status': owner_status
            })
        
        return JsonResponse({
            'users': users,
            'total_users': len(users)
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'users': []
        })

def debug_images(request):
    """Debug view to test image URLs"""
    dogs = Dog.objects.all()
    debug_info = []
    
    for dog in dogs:
        info = {
            'name': dog.name,
            'photo_field': str(dog.photo),
            'photo_url': dog.get_photo_url(),
            'photo_exists': bool(dog.photo),
            'photo_name': dog.photo.name if dog.photo else None,
        }
        debug_info.append(info)
    
    return render(request, 'core/debug_images.html', {'debug_info': debug_info})

def test_images_simple(request):
    """Simple test view for images - safe version"""
    try:
        dogs = Dog.objects.all()
        return render(request, 'core/test_images.html', {'dogs': dogs})
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

def test_basic(request):
    """Very basic test view - no database access"""
    return HttpResponse("Basic test page is working! No database access.")

def test_deployment(request):
    """Simple test view to verify deployment is working"""
    return HttpResponse("✅ Deployment is working! Database issues are being resolved.")

def create_test_dog(request):
    """Create a test dog for testing purposes"""
    try:
        # Get or create test owner
        test_user, created = User.objects.get_or_create(
            username='testowner',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'Owner'
            }
        )
        
        if created:
            test_user.set_password('test123456')
            test_user.save()
            
            # Create Owner record
            Owner.objects.create(
                user=test_user,
                phone='555-1234',
                address='123 Test Street'
            )
        
        # Get the owner
        owner = Owner.objects.get(user=test_user)
        
        # Create a test dog if it doesn't exist
        if not Dog.objects.filter(owner=owner, name='Buddy').exists():
            # Use raw SQL to avoid the photo_base64 column issue
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO core_dog (owner_id, name, breed, age, size, notes, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                """, [owner.id, 'Buddy', 'Golden Retriever', 3, 'large', 'A friendly test dog for testing the application.'])
                
                # Get the created dog's ID
                dog_id = cursor.lastrowid if hasattr(cursor, 'lastrowid') else cursor.execute("SELECT LASTVAL()").fetchone()[0]
                
            return HttpResponse(f"✅ Test dog created! Dog ID: {dog_id}<br><br>You can now test:<br>- <a href='/dogs/{dog_id}/edit/'>Edit Dog</a><br>- <a href='/dashboard/'>Dashboard</a>")
        else:
            dog = Dog.objects.get(owner=owner, name='Buddy')
            return HttpResponse(f"✅ Test dog already exists! Dog ID: {dog.id}<br><br>You can test:<br>- <a href='/dogs/{dog.id}/edit/'>Edit Dog</a><br>- <a href='/dashboard/'>Dashboard</a>")
            
    except Exception as e:
        return HttpResponse(f"❌ Error creating test dog: {str(e)}")

@user_passes_test(is_staff)
def staff_daily_logs(request):
    """Staff view to manage daily logs"""
    # Get filter parameters
    date_filter = request.GET.get('date', '')
    booking_filter = request.GET.get('booking', '')
    dog_filter = request.GET.get('dog', '')
    
    # Get all logs
    logs = DailyLog.objects.all().order_by('-date', '-id')
    
    # Apply filters
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            logs = logs.filter(date=filter_date)
        except ValueError:
            pass
    
    if booking_filter:
        logs = logs.filter(booking_id=booking_filter)
    
    if dog_filter:
        logs = logs.filter(booking__dog__name__icontains=dog_filter)
    
    # Get all bookings for filter dropdown
    bookings = Booking.objects.filter(status='confirmed').order_by('-start_date')
    
    # Get unique dogs for filter dropdown
    dogs = Dog.objects.filter(bookings__status='confirmed').distinct().order_by('name')
    
    context = {
        'logs': logs,
        'bookings': bookings,
        'dogs': dogs,
        'date_filter': date_filter,
        'booking_filter': booking_filter,
        'dog_filter': dog_filter,
    }
    return render(request, 'core/staff_daily_logs.html', context)

@user_passes_test(is_staff)
def create_daily_log(request):
    """Create a new daily log"""
    if request.method == 'POST':
        booking_id = request.POST.get('booking')
        date_str = request.POST.get('date')
        feeding = request.POST.get('feeding', '')
        medication = request.POST.get('medication', '')
        exercise = request.POST.get('exercise', '')
        notes = request.POST.get('notes', '')
        
        try:
            # Parse the date string (mm/dd/yyyy format)
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%m/%d/%Y').date()
            
            booking = Booking.objects.get(id=booking_id)
            log = DailyLog.objects.create(
                booking=booking,
                date=date_obj,
                feeding=feeding,
                medication=medication,
                exercise=exercise,
                notes=notes
            )
            
            # Handle photo upload
            if 'photo' in request.FILES:
                log.photo = request.FILES['photo']
                log.save()
            
            # Send notification to owner
            send_log_notification_to_owner(log)
            
            messages.success(request, f"Daily log created for {booking.dog.name} on {date_str}")
            return redirect('staff_daily_logs')
        except Booking.DoesNotExist:
            messages.error(request, "Invalid booking selected")
        except ValueError:
            messages.error(request, "Invalid date format. Please use mm/dd/yyyy format.")
        except Exception as e:
            messages.error(request, f"Error creating log: {str(e)}")
    
    # Get active bookings for dropdown
    active_bookings = Booking.objects.filter(
        status='confirmed',
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date()
    ).order_by('dog__name')
    
    context = {
        'active_bookings': active_bookings,
        'today': timezone.now().date(),
    }
    return render(request, 'core/create_daily_log.html', context)

@user_passes_test(is_staff)
def edit_daily_log(request, log_id):
    """Edit an existing daily log"""
    log = get_object_or_404(DailyLog, id=log_id)
    
    if request.method == 'POST':
        date_str = request.POST.get('date')
        
        try:
            # Parse the date string (mm/dd/yyyy format)
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%m/%d/%Y').date()
            
            log.date = date_obj
            log.feeding = request.POST.get('feeding', '')
            log.medication = request.POST.get('medication', '')
            log.exercise = request.POST.get('exercise', '')
            log.notes = request.POST.get('notes', '')
            
            # Handle photo upload
            if 'photo' in request.FILES:
                log.photo = request.FILES['photo']
            
            log.save()
            
            messages.success(request, f"Daily log updated for {log.booking.dog.name} on {date_str}")
            return redirect('staff_daily_logs')
        except ValueError:
            messages.error(request, "Invalid date format. Please use mm/dd/yyyy format.")
        except Exception as e:
            messages.error(request, f"Error updating log: {str(e)}")
    
    context = {
        'log': log,
    }
    return render(request, 'core/edit_daily_log.html', context)

@user_passes_test(is_staff)
def delete_daily_log(request, log_id):
    """Delete a daily log"""
    if request.method == 'POST':
        log = get_object_or_404(DailyLog, id=log_id)
        dog_name = log.booking.dog.name
        log.delete()
        messages.success(request, f"Daily log deleted for {dog_name}")
        return redirect('staff_daily_logs')
    
    return redirect('staff_daily_logs')

@user_passes_test(is_staff)
def booking_daily_logs(request, booking_id):
    """View all daily logs for a specific booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    logs = DailyLog.objects.filter(booking=booking).order_by('date')
    
    context = {
        'booking': booking,
        'logs': logs,
    }
    return render(request, 'core/booking_daily_logs.html', context)

@user_passes_test(is_staff)
def daily_log_detail(request, log_id):
    """View detailed information for a specific daily log"""
    log = get_object_or_404(DailyLog, id=log_id)
    
    context = {
        'log': log,
    }
    return render(request, 'core/daily_log_detail.html', context)

# Add this new view after the existing views

@login_required
@user_passes_test(is_owner)
def owner_daily_logs(request):
    """Owner view to see their dog's daily logs"""
    # Get the owner
    try:
        owner = Owner.objects.get(user=request.user)
    except Owner.DoesNotExist:
        messages.error(request, "Owner profile not found.")
        return redirect('dashboard')
    
    # Get filter parameters
    dog_filter = request.GET.get('dog', '')
    date_filter = request.GET.get('date', '')
    
    # Get all bookings for this owner's dogs
    bookings = Booking.objects.filter(dog__owner=owner).order_by('-start_date')
    
    # Get all logs for these bookings
    logs = DailyLog.objects.filter(booking__in=bookings).order_by('-date', '-id')
    
    # Apply filters
    if dog_filter:
        logs = logs.filter(booking__dog_id=dog_filter)
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            logs = logs.filter(date=filter_date)
        except ValueError:
            pass
    
    # Get unique dogs for filter dropdown
    dogs = Dog.objects.filter(owner=owner).order_by('name')
    
    context = {
        'logs': logs,
        'dogs': dogs,
        'dog_filter': dog_filter,
        'date_filter': date_filter,
        'owner': owner,
    }
    return render(request, 'core/owner_daily_logs.html', context)

@login_required
@user_passes_test(is_owner)
def owner_dog_logs(request, dog_id):
    """Owner view to see logs for a specific dog"""
    try:
        dog = Dog.objects.get(id=dog_id, owner__user=request.user)
    except Dog.DoesNotExist:
        messages.error(request, "Dog not found or you don't have permission to view it.")
        return redirect('owner_daily_logs')
    
    # Get all logs for this dog's bookings
    logs = DailyLog.objects.filter(booking__dog=dog).order_by('-date', '-id')
    
    context = {
        'dog': dog,
        'logs': logs,
    }
    return render(request, 'core/owner_dog_logs.html', context)

@user_passes_test(is_staff)
def export_daily_logs(request):
    """Export daily logs as CSV for reporting"""
    # Get filter parameters
    date_filter = request.GET.get('date', '')
    booking_filter = request.GET.get('booking', '')
    dog_filter = request.GET.get('dog', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    # Get all logs
    logs = DailyLog.objects.all().order_by('-date', '-id')
    
    # Apply filters
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            logs = logs.filter(date=filter_date)
        except ValueError:
            pass
    
    if booking_filter:
        logs = logs.filter(booking_id=booking_filter)
    
    if dog_filter:
        logs = logs.filter(booking__dog__name__icontains=dog_filter)
    
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            logs = logs.filter(date__gte=start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            logs = logs.filter(date__lte=end)
        except ValueError:
            pass
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="daily_logs_{timezone.now().date()}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Date',
        'Dog Name',
        'Dog Breed',
        'Owner Name',
        'Kennel',
        'Feeding',
        'Medication',
        'Exercise',
        'Notes',
        'Photo URL'
    ])
    
    for log in logs:
        writer.writerow([
            log.date.strftime('%m/%d/%Y'),
            log.booking.dog.name,
            log.booking.dog.breed or 'Mixed breed',
            log.booking.dog.owner.user.get_full_name() or log.booking.dog.owner.user.username,
            log.booking.kennel.name if log.booking.kennel else 'Not assigned',
            log.feeding,
            log.medication,
            log.exercise,
            log.notes,
            log.photo.url if log.photo else ''
        ])
    
    return response

def send_log_notification_to_owner(log):
    """Send email notification to owner when a daily log is created"""
    try:
        booking = log.booking
        owner = booking.dog.owner
        owner_email = owner.user.email
        
        if not owner_email:
            print(f"No email found for owner {owner.user.username}")
            return False
        
        subject = f"Daily Log Update for {booking.dog.name}"
        
        # Format the date as mm/dd/yyyy
        log_date = log.date.strftime('%m/%d/%Y')
        
        message = f"""
Hello {owner.user.first_name or owner.user.username},

A daily log has been created for {booking.dog.name} on {log_date}.

Log Details:
- Feeding: {log.feeding or 'Not specified'}
- Medication: {log.medication or 'Not specified'}
- Exercise: {log.exercise or 'Not specified'}
- Notes: {log.notes or 'No additional notes'}

You can view all logs for {booking.dog.name} by logging into your account.

Best regards,
The Dog Boarding Team
        """
        
        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [owner_email],
            fail_silently=False,
        )
        
        print(f"Email notification sent to {owner_email}")
        return True
        
    except Exception as e:
        print(f"Error sending email notification: {e}")
        return False

@login_required
def user_profile(request):
    """User profile page for updating personal information"""
    user = request.user
    
    if request.method == 'POST':
        # Handle form submission
        action = request.POST.get('action')
        
        if action == 'update_profile':
            # Update basic profile information
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name = request.POST.get('last_name', '').strip()
            user.email = request.POST.get('email', '').strip()
            
            # Update owner phone if user is an owner
            try:
                owner = Owner.objects.get(user=user)
                owner.phone = request.POST.get('phone', '').strip()
                owner.save()
            except Owner.DoesNotExist:
                pass
            
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
            
        elif action == 'change_password':
            # Handle password change
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
            else:
                user.set_password(new_password)
                user.save()
                # Re-login the user after password change
                from django.contrib.auth import login
                login(request, user)
                messages.success(request, 'Password changed successfully!')
                return redirect('user_profile')
    
    # Get owner information if user is an owner
    owner = None
    try:
        owner = Owner.objects.get(user=user)
    except Owner.DoesNotExist:
        pass
    
    context = {
        'user': user,
        'owner': owner,
    }
    return render(request, 'core/user_profile.html', context)
