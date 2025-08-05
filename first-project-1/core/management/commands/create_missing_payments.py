from django.core.management.base import BaseCommand
from core.models import Booking, Payment
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create missing payment records for existing bookings'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Creating missing payment records...')
        
        # Get all confirmed bookings that don't have payment records
        bookings_without_payments = Booking.objects.filter(
            status='confirmed'
        ).exclude(
            payment__isnull=False
        )
        
        if not bookings_without_payments.exists():
            self.stdout.write(
                self.style.SUCCESS('✅ All confirmed bookings already have payment records')
            )
            return
        
        self.stdout.write(f'📋 Found {bookings_without_payments.count()} bookings without payment records')
        
        created_count = 0
        
        for booking in bookings_without_payments:
            try:
                # Use the model's calculate_total method for correct pricing
                total_amount = booking.calculate_total()
                
                # Create payment record
                Payment.objects.create(
                    booking=booking,
                    amount=total_amount,
                    status='pending'
                )
                
                # Save the booking with updated pricing info
                booking.save()
                
                created_count += 1
                self.stdout.write(
                    f'✅ Created payment for {booking.dog.name}: ${total_amount} ({nights} nights)'
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error creating payment for {booking.dog.name}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Created {created_count} payment records successfully!')
        ) 