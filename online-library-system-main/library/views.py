from library.forms import IssueBookForm
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from .forms import IssueBookForm
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from .models import IssuedBook  
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .utils import fetch_book_details
import requests
from django.http import JsonResponse


def index(request):
    return render(request, "index.html")

@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
        isbn = request.POST.get('isbn')
        if isbn:
            # Check if book already exists
            existing_book = Book.objects.filter(isbn=isbn).first()
            if existing_book:
                messages.warning(request, 'This book already exists in the library.')
                return render(request, "add_book.html", {'book': existing_book})
            
            # Fetch book details from Google Books API
            book_details = fetch_book_details(isbn)
            if book_details:
                try:
                    book = Book.objects.create(
                        name=book_details['name'],
                        author=book_details['author'],
                        isbn=isbn,
                        category=book_details['category'],
                        description=book_details['description'],
                        page_count=book_details['page_count'],
                        thumbnail_url=book_details['thumbnail']
                    )
                    messages.success(request, 'Book added successfully!')
                    return render(request, "add_book.html", {'book': book, 'success': True})
                except Exception as e:
                    print(f"Error creating book: {str(e)}")
                    messages.error(request, f'Error saving book: {str(e)}')
            else:
                messages.error(request, 'Book not found. Please check the ISBN.')
        else:
            messages.error(request, 'ISBN is required.')
            
    return render(request, "add_book.html")

@login_required(login_url = '/admin_login')
def view_books(request):
    try:
        books = Book.objects.all()
        
        # Get unique categories and sort them
        categories = sorted(set(Book.objects.exclude(category__isnull=True)
                          .exclude(category__exact='')
                          .values_list('category', flat=True)
                          .distinct()))
        
        # Handle search
        search_query = request.GET.get('search', '')
        if search_query:
            books = books.filter(
                models.Q(name__icontains=search_query) |
                models.Q(author__icontains=search_query) |
                models.Q(isbn__icontains=search_query)
            )
        
        # Handle category filter
        category_filter = request.GET.get('category', '')
        if category_filter:
            books = books.filter(category__iexact=category_filter)
            
        # Handle sorting
        sort_by = request.GET.get('sort', '-added_date')
        books = books.order_by(sort_by)
        
        return render(request, "view_books.html", {
            'books': books,
            'categories': categories,
            'search_query': search_query,
            'selected_category': category_filter,
            'sort_by': sort_by
        })
    except Exception as e:
        messages.error(request, f'Error loading books: {str(e)}')
        return render(request, "view_books.html", {
            'books': [],
            'categories': [],
            'search_query': '',
            'selected_category': '',
            'sort_by': '-added_date'
        })

@login_required(login_url = '/student_login')
def student_view_books(request):
    books = Book.objects.all()
    return render(request, "student_view_books.html", {'books':books})

@login_required(login_url = '/admin_login')
def view_students(request):
    students = Student.objects.all()
    return render(request, "view_students.html", {'students':students})

@login_required(login_url = '/admin_login')
def issue_book(request):
    form = forms.IssueBookForm()
    if request.method == "POST":
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.student_id = request.POST['name2']
            obj.isbn = request.POST['isbn2']
            obj.save()
            alert = True
            return render(request, "issue_book.html", {'obj':obj, 'alert':alert})
    return render(request, "issue_book.html", {'form':form})

@login_required(login_url = '/admin_login')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for issued_book in issuedBooks:
        days = (date.today()-issued_book.issued_date)
        d = days.days
        fine = 0
        if d > 14:
            overdue_days = d - issued_book.expiry_date.day
            fine = overdue_days * 2
        books = list(models.Book.objects.filter(isbn=issued_book.isbn))
        students = list(models.Student.objects.filter(user=issued_book.student_id))
        
        if books and students:  
            t = (students[0].user, students[0].user_id, books[0].name, books[0].isbn,
                issued_book.issued_date, issued_book.expiry_date, fine)
            details.append(t)
            
    return render(request, "view_issued_book.html", {'issuedBooks':issuedBooks, 'details':details})

@login_required(login_url = '/student_login')
def student_issued_books(request):
    student = Student.objects.filter(user_id=request.user.id)
    if not student:
        return render(request, 'student_issued_books.html', {'li1': [], 'li2': []})
        
    issuedBooks = IssuedBook.objects.filter(student_id=student[0].user_id)
    if not issuedBooks:
        return render(request, 'student_issued_books.html', {'li1': [], 'li2': []})
        
    li1 = []
    li2 = []

    for issued_book in issuedBooks:
        books = Book.objects.filter(isbn=issued_book.isbn)
        if books:
            book = books[0]
            t = (request.user.id, request.user.get_full_name(), book.name, book.author)
            li1.append(t)
            
            days = (date.today() - issued_book.issued_date)
            d = days.days
            fine = 0
            if date.today() > issued_book.expiry_date:
                overdue_days = (date.today() - issued_book.expiry_date).days
                fine = overdue_days * 2
            t = (issued_book.issued_date, issued_book.expiry_date, fine)
            li2.append(t)
            
    return render(request, 'student_issued_books.html', {'li1': li1, 'li2': li2})

@login_required(login_url = '/student_login')
def profile(request):
    try:
        student = Student.objects.get(user=request.user)
        return render(request, "profile.html", {'student': student})
    except Student.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('edit_profile')

@login_required(login_url = '/student_login')
def edit_profile(request):
    try:
        student = Student.objects.get(user=request.user)
        if request.method == "POST":
            email = request.POST['email']
            phone = request.POST['phone']
            branch = request.POST['branch']
            classroom = request.POST['classroom']
            roll_no = request.POST['roll_no']
            
            # Handle image upload
            if 'image' in request.FILES:
                student.image = request.FILES['image']

            student.user.email = email
            student.phone = phone
            student.branch = branch
            student.classroom = classroom
            student.roll_no = roll_no
            student.user.save()
            student.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
            
        return render(request, "edit_profile.html", {'student': student})
        
    except Student.DoesNotExist:
        if request.method == "POST":
            email = request.POST['email']
            phone = request.POST['phone']
            branch = request.POST['branch']
            classroom = request.POST['classroom']
            roll_no = request.POST['roll_no']
            
            try:
                student = Student.objects.create(
                    user=request.user,
                    phone=phone,
                    branch=branch,
                    classroom=classroom,
                    roll_no=roll_no
                )
                
                # Handle image upload for new profile
                if 'image' in request.FILES:
                    student.image = request.FILES['image']
                    student.save()
                    
                request.user.email = email
                request.user.save()
                messages.success(request, 'Profile created successfully!')
                return redirect('profile')
            except Exception as e:
                messages.error(request, f'Error creating profile: {str(e)}')
                
        return render(request, "edit_profile.html", {'new_profile': True})

@login_required(login_url = '/student_login')
def request_book(request, book_id):
    try:
        # Get or create student profile
        student = Student.objects.get(user=request.user)
        book = Book.objects.get(id=book_id)
        
        # Check if student already has a pending request for this book
        existing_request = BookRequest.objects.filter(
            student=student,
            book=book,
            status='pending'
        ).first()
        
        if existing_request:
            messages.warning(request, 'You already have a pending request for this book.')
        else:
            # Create new book request
            book_request = BookRequest.objects.create(
                student=student,
                book=book
            )
            messages.success(request, 'Book request submitted successfully!')
            
        return redirect('student_view_books')
    except Student.DoesNotExist:
        messages.error(request, 'Please complete your student profile before requesting books.')
        return redirect('edit_profile')
    except Book.DoesNotExist:
        messages.error(request, 'Book not found.')
        return redirect('student_view_books')

@login_required(login_url = '/student_login')
def view_requests(request):
    try:
        student = Student.objects.get(user=request.user)
        book_requests = BookRequest.objects.filter(student=student).order_by('-request_date')
        return render(request, 'view_requests.html', {'requests': book_requests})
    except Student.DoesNotExist:
        # Handle case where student profile doesn't exist
        return render(request, 'view_requests.html', {'requests': [], 'error': 'Student profile not found'})

def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/view_books")

def delete_issue(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/student_issued_books")

def delete_student(request, myid):
    students = Student.objects.filter(id=myid)
    students.delete()
    return redirect("/view_students")

def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "change_password.html")

def student_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, "student_registration.html")

        try:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return render(request, "student_registration.html")

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create student profile
            student = Student.objects.create(
                user=user,
                phone=phone,
                branch=branch,
                classroom=classroom,
                roll_no=roll_no
            )
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('student_login')

        except Exception as e:
            # If any error occurs, delete the user if it was created
            if 'user' in locals():
                user.delete()
            messages.error(request, f'Error during registration: {str(e)}')
            return render(request, "student_registration.html")

    return render(request, "student_registration.html")

def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            # Check if user has a student profile
            try:
                student = Student.objects.get(user=user)
                if user.is_superuser:
                    messages.error(request, 'Admin users cannot login as students.')
                    return render(request, "student_login.html")
                else:
                    login(request, user)
                    return redirect("/profile")
            except Student.DoesNotExist:
                messages.error(request, 'No student profile found for this account.')
                return render(request, "student_login.html")
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, "student_login.html")
            
    return render(request, "student_login.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/view_students")  #add the new admin home page here
            else:
                return HttpResponse("Invalid Password or Username")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")

def Logout(request):
    logout(request)
    return redirect("/")

@login_required(login_url = '/admin_login')
def manage_book_requests(request):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=401)
        
    if request.method == "POST":
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        loan_duration = request.POST.get('loan_duration', 14)
        
        try:
            book_request = BookRequest.objects.get(id=request_id)
            
            if action == 'approve':
                # Check if book is already issued
                existing_issue = IssuedBook.objects.filter(
                    isbn=book_request.book.isbn,
                    student_id=book_request.student.user.id,
                    returned_date__isnull=True
                ).exists()
                
                if existing_issue:
                    messages.error(request, 'This book is already issued to this student.')
                else:
                    # Create new issue record
                    issue = IssuedBook.objects.create(
                        student_id=str(book_request.student.user.id),
                        isbn=book_request.book.isbn,
                        expiry_date=date.today() + timedelta(days=int(loan_duration))
                    )
                    book_request.status = 'approved'
                    book_request.approved_date = timezone.now()
                    book_request.loan_duration = loan_duration
                    book_request.save()
                    messages.success(request, 'Book request approved and book issued successfully.')
            
            elif action == 'reject':
                book_request.status = 'rejected'
                book_request.save()
                messages.success(request, 'Book request rejected.')
                
        except BookRequest.DoesNotExist:
            messages.error(request, 'Book request not found.')
        except Exception as e:
            messages.error(request, f'Error processing request: {str(e)}')
            
    pending_requests = BookRequest.objects.filter(status='pending').order_by('-request_date')
    processed_requests = BookRequest.objects.exclude(status='pending').order_by('-request_date')[:10]
    
    return render(request, "manage_book_requests.html", {
        'pending_requests': pending_requests,
        'processed_requests': processed_requests
    })

@login_required(login_url = '/admin_login')
def search_books(request):
    books = []
    categories = [
        'Fiction', 'Science', 'History', 'Technology', 'Philosophy',
        'Psychology', 'Business', 'Art', 'Poetry', 'Biography',
        'Mathematics', 'Computer Science', 'Medicine', 'Law', 'Economics'
    ]
    
    if request.method == "GET":
        category = request.GET.get('category', '')
        page = int(request.GET.get('page', 1))
        if category:
            try:
                # Calculate start index for pagination
                start_index = (page - 1) * 40
                url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{category}&maxResults=40&startIndex={start_index}"
                response = requests.get(url)
                data = response.json()
                
                total_items = data.get('totalItems', 0)
                has_more = total_items > (page * 40)
                
                if 'items' in data:
                    for item in data['items']:
                        book_info = item['volumeInfo']
                        # Get ISBN (prefer ISBN-13, fallback to ISBN-10)
                        isbn = None
                        for identifier in book_info.get('industryIdentifiers', []):
                            if identifier['type'] == 'ISBN_13':
                                isbn = identifier['identifier']
                                break
                            elif identifier['type'] == 'ISBN_10':
                                isbn = identifier['identifier']
                        
                        if isbn:  # Only add books with valid ISBNs
                            books.append({
                                'title': book_info.get('title', ''),
                                'authors': ', '.join(book_info.get('authors', [])),
                                'isbn': isbn,
                                'description': book_info.get('description', ''),
                                'categories': category,
                                'page_count': book_info.get('pageCount', 0),
                                'thumbnail': book_info.get('imageLinks', {}).get('thumbnail', ''),
                                'preview_link': book_info.get('previewLink', '')
                            })
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    # Return JSON response for AJAX requests
                    from django.template.loader import render_to_string
                    html = render_to_string('book_cards.html', {'books': books})
                    return JsonResponse({
                        'html': html,
                        'has_more': has_more
                    })
                    
            except Exception as e:
                messages.error(request, f'Error fetching books: {str(e)}')
    
    return render(request, "search_books.html", {
        'books': books,
        'categories': categories,
        'selected_category': category,
        'current_page': page,
        'has_more': has_more if category else False
    })

@login_required(login_url = '/admin_login')
def add_book_from_api(request):
    if request.method == "POST":
        try:
            title = request.POST.get('title')
            author = request.POST.get('author')
            isbn = request.POST.get('isbn')
            description = request.POST.get('description')
            category = request.POST.get('category')
            page_count = request.POST.get('page_count')
            thumbnail_url = request.POST.get('thumbnail')
            
            # Check if book already exists
            if Book.objects.filter(isbn=isbn).exists():
                messages.warning(request, 'This book already exists in the library.')
                return redirect('search_books')
            
            # Create new book
            book = Book.objects.create(
                name=title,
                author=author,
                isbn=isbn,
                category=category,
                description=description,
                page_count=page_count,
                thumbnail_url=thumbnail_url
            )
            messages.success(request, 'Book added successfully to library!')
            
        except Exception as e:
            messages.error(request, f'Error adding book: {str(e)}')
            
    return redirect('search_books')