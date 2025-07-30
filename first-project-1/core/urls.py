from django.urls import path
from . import views
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_owner, name='register_owner'),
    path('login/', views.login_owner, name='login_owner'),
    path('create-admin/', views.create_admin_user, name='create_admin_user'),
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('dogs/add/', views.add_dog, name='add_dog'),
    path('dogs/<int:dog_id>/edit/', views.edit_dog, name='edit_dog'),
    path('dogs/<int:dog_id>/delete/', views.delete_dog, name='delete_dog'),
    path('booking/calendar/', views.booking_calendar, name='booking_calendar'),
    path('booking/create/', views.create_booking, name='create_booking'),
    path('booking/list/', views.booking_list, name='booking_list'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    # Staff URLs
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/bookings/', views.staff_booking_list, name='staff_booking_list'),
    path('staff/bookings/<int:booking_id>/', views.staff_booking_detail, name='staff_booking_detail'),
    path('staff/kennels/', views.staff_kennel_management, name='staff_kennel_management'),
    path('staff/kennels/<int:kennel_id>/edit/', views.edit_kennel, name='edit_kennel'),
    path('staff/payments/', views.staff_payment_list, name='staff_payment_list'),
    path('staff/payments/<int:payment_id>/', views.staff_payment_detail, name='staff_payment_detail'),
    path('staff/calendar/', views.staff_calendar, name='staff_calendar'),
    path('staff/calendar/delete/<int:entry_id>/', views.delete_availability_entry, name='delete_availability_entry'),
    
] 
