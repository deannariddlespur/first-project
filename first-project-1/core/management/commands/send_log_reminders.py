from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from core.models import Booking, DailyLog
from datetime import date, timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send reminders to staff about creating daily logs for active bookings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending',
        )
        parser.add_argument(
            '--email',
            action='store_true',
            help='Send email reminders (requires email configuration)',
        )

    def handle(self, *args, **options):
        # Temporarily disabled due to database column issues
        self.stdout.write(
            self.style.WARNING('⚠️ Daily log reminders temporarily disabled due to database maintenance')
        )
        self.stdout.write(
            self.style.SUCCESS('✅ This feature will be re-enabled once database issues are resolved')
        )
        return
    
    def send_email_reminder(self, booking):
        """
        Send email reminder to staff about creating a daily log
        In a real implementation, this would use Django's email system
        """
        try:
            # This is a placeholder for email functionality
            # You would implement actual email sending here
            subject = f"Daily Log Reminder: {booking.dog.name}"
            message = f"""
            Hi Staff,
            
            Please create a daily log for {booking.dog.name} (Owner: {booking.dog.owner.user.get_full_name() or booking.dog.owner.user.username}).
            
            Booking Details:
            - Dog: {booking.dog.name} ({booking.dog.breed or 'Mixed breed'})
            - Owner: {booking.dog.owner.user.get_full_name() or booking.dog.owner.user.username}
            - Kennel: {booking.kennel.name if booking.kennel else 'Not assigned'}
            - Stay: {booking.start_date} to {booking.end_date}
            
            Please log today's activities including feeding, exercise, medication, and any notes.
            
            Thanks!
            """
            
            # For now, just log the message
            logger.info(f"Would send email reminder: {subject}")
            
        except Exception as e:
            logger.error(f"Error sending email reminder: {e}")
    
    def get_staff_users(self):
        """Get all staff users who should receive reminders"""
        return User.objects.filter(is_staff=True, is_active=True) 