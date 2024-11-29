from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.utils import timezone


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    page_count = models.IntegerField(default=0)
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
    added_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} [{self.isbn}]"

    class Meta:
        ordering = ['-added_date']

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=3, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="", blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.branch)+']' + " ["+str(self.classroom)+']' + " ["+str(self.roll_no)+']'


def expiry():
    return datetime.today() + timedelta(days=14)

class IssuedBook(models.Model):
    student_id = models.CharField(max_length=100, blank=True) 
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Book {self.isbn} issued to student {self.student_id}"

class BookRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')
    loan_duration = models.IntegerField(default=14, help_text="Duration in days")
    approved_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'book', 'status')

    def __str__(self):
        return f"{self.student.user.username} - {self.book.name} ({self.status})"
