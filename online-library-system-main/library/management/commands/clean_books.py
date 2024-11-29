from django.core.management.base import BaseCommand
from library.models import Book

class Command(BaseCommand):
    help = 'Clean all books from the database'

    def handle(self, *args, **kwargs):
        try:
            # Get the count before deletion
            count = Book.objects.count()
            
            # Delete all books
            Book.objects.all().delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {count} books from the database')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error cleaning database: {str(e)}')
            ) 