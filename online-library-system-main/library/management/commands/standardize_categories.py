from django.core.management.base import BaseCommand
from library.models import Book

class Command(BaseCommand):
    help = 'Standardize book categories in the database'

    # Define standard categories
    STANDARD_CATEGORIES = {
        'Fiction', 'Science Fiction', 'Mystery', 'Romance', 'History',
        'Biography', 'Business', 'Technology', 'Computer Science', 'Mathematics',
        'Physics', 'Chemistry', 'Biology', 'Medicine', 'Psychology',
        'Philosophy', 'Religion', 'Art', 'Music', 'Poetry',
        'Drama', 'Comics', 'Cooking', 'Travel', 'Sports'
    }

    # Category mapping for standardization
    CATEGORY_MAPPING = {
        # Fiction variants
        'fiction': 'Fiction',
        'novels': 'Fiction',
        'literary fiction': 'Fiction',
        'contemporary fiction': 'Fiction',
        
        # Science Fiction variants
        'sci-fi': 'Science Fiction',
        'sf': 'Science Fiction',
        'science fiction': 'Science Fiction',
        
        # Technology variants
        'tech': 'Technology',
        'computers': 'Technology',
        'engineering': 'Technology',
        'information technology': 'Technology',
        
        # Business variants
        'business & economics': 'Business',
        'economics': 'Business',
        'management': 'Business',
        'finance': 'Business',
        
        # Science variants
        'science': 'Science',
        'natural science': 'Science',
        'applied science': 'Science',
        
        # Computer Science variants
        'programming': 'Computer Science',
        'software': 'Computer Science',
        'coding': 'Computer Science',
        'development': 'Computer Science',
        
        # History variants
        'historical': 'History',
        'world history': 'History',
        'ancient history': 'History',
        
        # Biography variants
        'biographies': 'Biography',
        'autobiography': 'Biography',
        'memoir': 'Biography',
        
        # Medicine variants
        'medical': 'Medicine',
        'healthcare': 'Medicine',
        'health': 'Medicine',
        
        # Art variants
        'fine arts': 'Art',
        'visual arts': 'Art',
        'design': 'Art',
        
        # Music variants
        'musical': 'Music',
        'songs': 'Music',
        'instruments': 'Music',
        
        # Poetry variants
        'poems': 'Poetry',
        'verse': 'Poetry',
        'rhyme': 'Poetry',
        
        # Religion variants
        'religious': 'Religion',
        'spiritual': 'Religion',
        'theology': 'Religion',
        
        # Psychology variants
        'psychological': 'Psychology',
        'mental health': 'Psychology',
        'behavioral science': 'Psychology',
        
        # Philosophy variants
        'philosophical': 'Philosophy',
        'ethics': 'Philosophy',
        'logic': 'Philosophy',
        
        # Sports variants
        'athletics': 'Sports',
        'games': 'Sports',
        'physical education': 'Sports',
        
        # Comics variants
        'graphic novels': 'Comics',
        'manga': 'Comics',
        'comic books': 'Comics',
        
        # Cooking variants
        'food': 'Cooking',
        'culinary': 'Cooking',
        'recipes': 'Cooking',
        
        # Travel variants
        'tourism': 'Travel',
        'adventure': 'Travel',
        'geography': 'Travel',
    }

    def handle(self, *args, **kwargs):
        # Get all unique categories currently in the database
        current_categories = Book.objects.values_list('category', flat=True).distinct()
        
        # Counter for changes
        changes_made = 0
        
        self.stdout.write("Starting category standardization...")
        
        # Process each book
        for book in Book.objects.all():
            original_category = book.category.lower().strip()
            
            # Try to map the category
            if original_category in self.CATEGORY_MAPPING:
                new_category = self.CATEGORY_MAPPING[original_category]
                if book.category != new_category:
                    book.category = new_category
                    book.save()
                    changes_made += 1
                    self.stdout.write(f"Updated category for book '{book.name}': {original_category} → {new_category}")
            else:
                # Try to find the closest match in standard categories
                closest_match = None
                for std_cat in self.STANDARD_CATEGORIES:
                    if std_cat.lower() in original_category or original_category in std_cat.lower():
                        closest_match = std_cat
                        break
                
                if closest_match and book.category != closest_match:
                    book.category = closest_match
                    book.save()
                    changes_made += 1
                    self.stdout.write(f"Updated category for book '{book.name}': {original_category} → {closest_match}")
        
        self.stdout.write(self.style.SUCCESS(f"Successfully standardized {changes_made} book categories")) 