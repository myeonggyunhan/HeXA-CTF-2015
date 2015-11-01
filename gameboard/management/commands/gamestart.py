from django.core.management import BaseCommand
from gameboard.models import Entries

#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "Start CTF! Enable all problem entries... (set is_active=True)"

    # A command must define handle()
    def handle(self, *args, **options):
        self.stdout.write("Start CTF!")
	prob_entries = Entries.objects.all()
	for entry in prob_entries:
		entry.is_active = True
		entry.save()
