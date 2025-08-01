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
        today = timezone.now().date()
        dry_run = options['dry_run']
        send_email = options['email']
        
        self.stdout.write(
            self.style.SUCCESS(f'🔔 Starting daily log reminders for {today.strftime("%m/%d/%Y")}')
        )
        
        # Get active bookings (confirmed bookings that are currently ongoing)
        active_bookings = Booking.objects.filter(
            status='confirmed',
            start_date__lte=today,
            end_date__gte=today
        )
        
        if not active_bookings.exists():
            self.stdout.write(
                self.style.WARNING('⚠️ No active bookings found for today')
            )
            return
        
        self.stdout.write(f'📋 Found {active_bookings.count()} active bookings')
        
        reminders_sent = 0
        logs_missing = 0
        
        for booking in active_bookings:
            # Check if a log already exists for today
            existing_log = DailyLog.objects.filter(
                booking=booking,
                date=today
            ).first()
            
            if existing_log:
                self.stdout.write(
                    f'✅ Log already exists for {booking.dog.name} on {today}'
                )
                continue
            
            # Log is missing - create reminder
            logs_missing += 1
            
            if dry_run:
                self.stdout.write(
                    f'🔔 [DRY RUN] Would send reminder for {booking.dog.name} '
                    f'(Owner: {booking.dog.owner.user.get_full_name() or booking.dog.owner.user.username})'
                )
            else:
                # In a real implementation, you would send an email or notification here
                self.stdout.write(
                    f'🔔 Reminder: Create daily log for {booking.dog.name} '
                    f'(Owner: {booking.dog.owner.user.get_full_name() or booking.dog.owner.user.username})'
                )
                
                if send_email:
                    self.send_email_reminder(booking)
                
                reminders_sent += 1
        
        # Summary
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'📊 [DRY RUN] Would send {logs_missing} reminders')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'📊 Sent {reminders_sent} reminders for missing logs')
            )
    
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