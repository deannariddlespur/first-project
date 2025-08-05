from django.core.management.base import BaseCommand
from core.models import Booking, Payment
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create a test payment for debugging'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Creating test payment...')
        
        try:
            # Get the first confirmed booking
            booking = Booking.objects.filter(status='confirmed').first()
            
            if not booking:
                self.stdout.write(
                    self.style.ERROR('❌ No confirmed bookings found')
                )
                return
            
            self.stdout.write(f'📋 Found booking: {booking.dog.name} ({booking.start_date} to {booking.end_date})')
            
            # Use the model's calculate_total method for correct pricing
            total_amount = booking.calculate_total()
            
            # Create payment record
            payment = Payment.objects.create(
                booking=booking,
                amount=total_amount,
                status='pending'
            )
            
            # Save the booking with updated pricing info
            booking.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created payment: ${total_amount} for {booking.dog.name}')
            )
            self.stdout.write(f'📊 Payment ID: {payment.id}')
            self.stdout.write(f'📊 Booking ID: {booking.id}')
            self.stdout.write(f'📊 Nights: {nights}')
            self.stdout.write(f'📊 Price per night: ${price_per_night}')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating test payment: {e}')
            ) 