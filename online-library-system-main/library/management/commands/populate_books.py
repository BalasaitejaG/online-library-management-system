from django.core.management.base import BaseCommand
import requests
from library.models import Book
from django.utils import timezone
import time

class Command(BaseCommand):
    help = 'Populate the database with books from Google Books API'

    # Define standard categories
    categories = [
        'Fiction', 'Science Fiction', 'Mystery', 'Romance', 'History',
        'Biography', 'Business', 'Technology', 'Computer Science', 'Mathematics',
        'Physics', 'Chemistry', 'Biology', 'Medicine', 'Psychology',
        'Philosophy', 'Religion', 'Art', 'Music', 'Poetry',
        'Drama', 'Comics', 'Cooking', 'Travel', 'Sports'
    ]
    
    # Define category mapping as class attribute
    category_mapping = {
        'Sci-Fi': 'Science Fiction',
        'Science': 'Science',
        'Historical': 'History',
        'Historical Fiction': 'Fiction',
        'Biographies': 'Biography',
        'Business & Economics': 'Business',
        'Programming': 'Computer Science',
        'Software': 'Computer Science',
        'Medical': 'Medicine',
        'Health': 'Medicine',
        'Religious': 'Religion',
        'Fine Arts': 'Art',
        'Musical': 'Music',
        'Poems': 'Poetry',
        'Theater': 'Drama',
        'Graphic Novels': 'Comics',
        'Food': 'Cooking',
        'Tourism': 'Travel',
        'Athletics': 'Sports'
    }

    def handle(self, *args, **kwargs):
        books_added = 0
        books_per_category = 40
        
        for category in self.categories:  # Use self.categories
            self.stdout.write(f'Fetching {category} books...')
            try:
                for offset in range(0, books_per_category, 20):
                    url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{category}&maxResults=20&startIndex={offset}"
                    response = requests.get(url)
                    data = response.json()
                    
                    if 'items' in data:
                        for item in data['items']:
                            book_info = item['volumeInfo']
                            
                            # Get ISBN
                            isbn = None
                            for identifier in book_info.get('industryIdentifiers', []):
                                if identifier['type'] == 'ISBN_13':
                                    isbn = identifier['identifier']
                                    break
                                elif identifier['type'] == 'ISBN_10':
                                    isbn = identifier['identifier']
                            
                            # Only add books with valid ISBNs and that don't already exist
                            if isbn and not Book.objects.filter(isbn=isbn).exists():
                                try:
                                    # Map the category to a standard category if needed
                                    book_category = category
                                    api_categories = book_info.get('categories', [])
                                    if api_categories:
                                        # Try to map the first API category to our standard categories
                                        api_category = api_categories[0].strip()
                                        book_category = self.category_mapping.get(api_category, category)  # Use self.category_mapping
                                    
                                    Book.objects.create(
                                        name=book_info.get('title', '')[:200],
                                        author=', '.join(book_info.get('authors', ['Unknown']))[:200],
                                        isbn=isbn,
                                        category=book_category,
                                        description=book_info.get('description', '')[:1000] if book_info.get('description') else '',
                                        page_count=book_info.get('pageCount', 0),
                                        thumbnail_url=book_info.get('imageLinks', {}).get('thumbnail', ''),
                                        added_date=timezone.now()
                                    )
                                    books_added += 1
                                    
                                    if books_added % 20 == 0:
                                        self.stdout.write(f'Added {books_added} books...')
                                        
                                except Exception as e:
                                    self.stdout.write(self.style.WARNING(f'Error adding book {isbn}: {str(e)}'))
                    
                    time.sleep(1)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error fetching {category} books: {str(e)}'))
                continue
                
        self.stdout.write(self.style.SUCCESS(f'Successfully added {books_added} books')) 