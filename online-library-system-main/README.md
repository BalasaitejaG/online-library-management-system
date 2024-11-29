# Online Library Management System

This project is a web-based Online Library Management System built using the Django framework along with HTML and CSS for the frontend. It allows students to create accounts and access the library's book collection. The admin has complete control over the system, including managing student information, books, and fines for overdue books.

## Features

- **Student Accounts:** Allows students to create accounts and access the library's collection.
- **Admin Dashboard:** Admins have complete control over student information and book inventory.
- **Book Management:** Efficiently manage the library's book inventory.
- **Fine Management:** Automatically calculates fines for overdue books.
- **User-Friendly Interface:** Intuitive and easy-to-use interface for both students and admins.
- **Book Search & Filter:** Search and filter books by category, author, or title.
- **Auto-population:** Easily populate your library with 1000+ books from various categories.

## Technologies Used

- **Python**
- **Django**: For building the web application.
- **HTML/CSS**: For the frontend design.

## Requirements

- Python 3.x
- Django
- SQLite (default database for Django)

## Installation

1. Clone the repository:
    ```sh
    https://github.com/BalasaitejaG/Library_managment_system.git
    ```
2. Change to the project directory:
    ```sh
    cd online-library-management-system
    ```
3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
      ```sh
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      source venv/bin/activate
      ```
5. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
6. Apply the migrations:
    ```sh
    python manage.py migrate
    ```
7. Populate the library with sample books (optional but recommended):
    ```sh
    python manage.py populate_books
    ```
    This command will add 1000 books from various categories using the Google Books API.

8. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

1. Open a web browser and navigate to `{Local host}`.
2. Create an admin account using the Django admin interface at `http://{Your local host}/admin/`.
3. Create student accounts and add books through the admin interface.
4. Students can log in to their accounts to browse and borrow books.

## Project Structure

- **LibraryManagementSystem/**: Main project directory.
- **db.sqlite3**: SQLite database file.
- **library/**: Django app for managing the library system.
- **manage.py**: Command-line utility for administrative tasks.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgments

- Thanks to the Django community for providing excellent documentation and support.
- Inspired by various open-source library management systems.
- Uses Google Books API for book data population.

