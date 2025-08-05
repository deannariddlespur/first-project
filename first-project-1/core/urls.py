from django.urls import path
from . import views
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health_check, name='health_check'),
    path('debug/', views.debug_app, name='debug_app'),
    path('fix-dog-ownership/', views.fix_dog_ownership, name='fix_dog_ownership'),
    path('list-users/', views.list_users, name='list_users'),
    path('create-test-user/', views.create_test_user_simple, name='create_test_user_simple'),
    path('create-admin/', views.create_admin_user_simple, name='create_admin_user_simple'),
    path('create-test-dog/', views.create_test_dog, name='create_test_dog'),
    path('test-staff/', views.test_staff_status, name='test_staff_status'),
    path('register/', views.register_owner, name='register_owner'),
    path('login/', views.login_owner, name='login_owner'),
    path('logout/', views.logout_view, name='logout'),
    
    # Staff URLs
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/bookings/', views.staff_booking_list, name='staff_booking_list'),
    path('staff/bookings/<int:booking_id>/', views.staff_booking_detail, name='staff_booking_detail'),
    path('staff/kennels/', views.staff_kennel_management, name='staff_kennel_management'),
    path('staff/kennels/<int:kennel_id>/edit/', views.edit_kennel, name='edit_kennel'),
    path('staff/payments/', views.staff_payment_list, name='staff_payment_list'),
    path('staff/payments/<int:payment_id>/', views.staff_payment_detail, name='staff_payment_detail'),
    path('staff/calendar/', views.staff_calendar, name='staff_calendar'),
    path('staff/availability/<int:entry_id>/delete/', views.delete_availability_entry, name='delete_availability_entry'),
    
    # Daily Log URLs
    path('staff/daily-logs/', views.staff_daily_logs, name='staff_daily_logs'),
    path('staff/daily-logs/create/', views.create_daily_log, name='create_daily_log'),
    path('staff/daily-logs/<int:log_id>/edit/', views.edit_daily_log, name='edit_daily_log'),
    path('staff/daily-logs/<int:log_id>/delete/', views.delete_daily_log, name='delete_daily_log'),
    path('staff/daily-logs/<int:log_id>/', views.daily_log_detail, name='daily_log_detail'),
    path('staff/booking/<int:booking_id>/logs/', views.booking_daily_logs, name='booking_daily_logs'),
    path('staff/daily-logs/export/', views.export_daily_logs, name='export_daily_logs'),
    
    # Owner Daily Log URLs
    path('my-dogs/logs/', views.owner_daily_logs, name='owner_daily_logs'),
    path('my-dogs/<int:dog_id>/logs/', views.owner_dog_logs, name='owner_dog_logs'),
    
    # Database maintenance URLs
    path('fix-session-table/', views.fix_session_table, name='fix_session_table'),
    path('emergency-fix-database/', views.emergency_fix_database, name='emergency_fix_database'),
    path('setup-database/', views.setup_database, name='setup_database'),
    
    # Owner URLs
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('dogs/add/', views.add_dog, name='add_dog'),
    path('dogs/<int:dog_id>/edit/', views.edit_dog, name='edit_dog'),
    path('dogs/<int:dog_id>/delete/', views.delete_dog, name='delete_dog'),
    path('bookings/calendar/', views.booking_calendar, name='booking_calendar'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/available-kennels/', views.get_available_kennels, name='get_available_kennels'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('profile/', views.user_profile, name='user_profile'),
    
    # Debug URLs
    path('debug-images/', views.debug_images, name='debug_images'),
    path('debug-supabase/', views.debug_supabase_config, name='debug_supabase_config'),
    path('test-images/', views.test_images_simple, name='test_images_simple'),
    path('test-basic/', views.test_basic, name='test_basic'),
    path('test-deployment/', views.test_deployment, name='test_deployment'),
    path('test-debug-logs/', views.test_debug_logs, name='test_debug_logs'),
    path('test-photo-urls/', views.test_photo_urls, name='test_photo_urls'),
    path('test-supabase-upload/', views.test_supabase_upload, name='test_supabase_upload'),
    path('test-photo-field-length/', views.test_photo_field_length, name='test_photo_field_length'),
    path('debug-dog-photos/', views.debug_dog_photos, name='debug_dog_photos'),
    path('test-supabase-upload-debug/', views.test_supabase_upload_debug, name='test_supabase_upload_debug'),
] 
