from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.appointments.models import Appointment

class Command(BaseCommand):
    help = 'Обновляет статус записей, у которых истекло время'

    def handle(self, *args, **options):
        now = timezone.now()
        updated_count = Appointment.objects.filter(
            status='scheduled',
            time_slot__start_time__lt=now
        ).update(status='completed')
        print(f'Обновлено {updated_count} записей')
