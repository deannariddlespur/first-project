from django.urls import path
from . import views
from core import views
from .admin import dogboarding_admin

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health_check, name='health_check'),
    path('debug/', views.debug_app, name='debug_app'),
    path('list-users/', views.list_users, name='list_users'),
    path('create-test-user/', views.create_test_user_simple, name='create_test_user_simple'),
    path('register/', views.register_owner, name='register_owner'),
    path('login/', views.login_owner, name='login_owner'),
    path('logout/', views.logout_view, name='logout'),
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('dogs/add/', views.add_dog, name='add_dog'),
    path('dogs/<int:dog_id>/edit/', views.edit_dog, name='edit_dog'),
    path('dogs/<int:dog_id>/delete/', views.delete_dog, name='delete_dog'),
    path('bookings/calendar/', views.booking_calendar, name='booking_calendar'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('admin-dashboard/', dogboarding_admin.urls),
    path('debug-images/', views.debug_images, name='debug_images'),
    path('test-images/', views.test_images_simple, name='test_images_simple'),
    path('test-basic/', views.test_basic, name='test_basic'),
    path('test-deployment/', views.test_deployment, name='test_deployment'),
] 
