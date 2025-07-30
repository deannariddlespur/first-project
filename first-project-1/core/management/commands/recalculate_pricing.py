from django.core.management.base import BaseCommand
from core.models import Booking

class Command(BaseCommand):
    help = 'Recalculate pricing for all existing bookings'

    def handle(self, *args, **options):
        bookings = Booking.objects.all()
        updated_count = 0
        
        for booking in bookings:
            old_total = booking.total_amount
            old_price_per_night = booking.price_per_night
            
            # Recalculate pricing
            new_total = booking.calculate_total()
            booking.save()
            
            if old_total != booking.total_amount:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated booking {booking.id} ({booking.dog.name}): '
                        f'${old_total} → ${booking.total_amount} '
                        f'({booking.price_per_night}/night)'
                    )
                )
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated pricing for {updated_count} bookings'
            )
        ) 