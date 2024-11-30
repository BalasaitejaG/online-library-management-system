from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.index, name="index"),
    path("add_book/", views.add_book, name="add_book"),
    path("view_books/", views.view_books, name="view_books"),
    path("student_view_books/", views.student_view_books, name="student_view_books"),
    path("view_students/", views.view_students, name="view_students"),
    path("issue_book/", views.issue_book, name="issue_book"),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),

    path("student_registration/", views.student_registration, name="student_registration"),
    path("change_password/", views.change_password, name="change_password"),
    path("student_login/", views.student_login, name="student_login"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("logout/", views.Logout, name="logout"),

    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    path("delete_student/<int:myid>/", views.delete_student, name="delete_student"),
    path('delete_issue/<int:myid>/', views.delete_issue, name='delete_issue'),
    path('request_book/<int:book_id>/', views.request_book, name='request_book'),
    path('view_requests/', views.view_requests, name='view_requests'),
    path('manage_book_requests/', views.manage_book_requests, name='manage_book_requests'),
    path("search_books/", views.search_books, name="search_books"),
    path("add_book_from_api/", views.add_book_from_api, name="add_book_from_api"),
    path('student/login/', views.student_login, name='student_login'),
    path('student/register/', views.student_registration, name='student_registration'),
]