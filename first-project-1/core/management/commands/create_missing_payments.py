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
                # Calculate the amount based on kennel size and length of stay
                nights = (booking.end_date - booking.start_date).days
                
                # Default pricing if no kennel is assigned
                if booking.kennel:
                    # Use kennel-based pricing
                    if booking.kennel.size == 'small':
                        price_per_night = Decimal('25.00')
                    elif booking.kennel.size == 'medium':
                        price_per_night = Decimal('35.00')
                    else:  # large
                        price_per_night = Decimal('50.00')
                else:
                    # Default to medium kennel pricing
                    price_per_night = Decimal('35.00')
                
                total_amount = price_per_night * nights
                
                # Create payment record
                Payment.objects.create(
                    booking=booking,
                    amount=total_amount,
                    status='pending'
                )
                
                # Update booking with pricing info
                booking.price_per_night = price_per_night
                booking.total_amount = total_amount
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