import requests

def fetch_book_details(isbn):
    """Fetch book details from Google Books API"""
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        response = requests.get(url)
        data = response.json()
        
        if data.get('items'):
            book_info = data['items'][0]['volumeInfo']
            return {
                'name': book_info.get('title', ''),
                'author': ', '.join(book_info.get('authors', ['Unknown'])),
                'isbn': isbn,
                'category': ', '.join(book_info.get('categories', ['Uncategorized'])),
                'description': book_info.get('description', 'No description available'),
                'page_count': book_info.get('pageCount', 0),
                'thumbnail': book_info.get('imageLinks', {}).get('thumbnail', '')
            }
        print(f"No books found for ISBN: {isbn}")
        return None
    except Exception as e:
        print(f"Error fetching book details: {str(e)}")
        return None 