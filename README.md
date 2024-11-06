# API Book Registration and Evaluation

A Django-based REST API for managing and evaluating books, allowing users to register books, rate them, and get random book recommendations based on various filters.

![alfons-morales-YLSwjSy7stw-unsplash](https://github.com/user-attachments/assets/e1db1883-831d-4bce-bf4c-cb9812c8eeb3)


## 🎯 Project Overview

This is an MVP (Minimum Viable Product) project that provides a RESTful API for:
- Book registration and management
- Book ratings and evaluations
- Random book recommendations with customizable filters
- Category-based book organization

## 🛠️ Technologies Used

- Python
- Django
- Django Ninja (for REST API)
- SQLite (default Django database)

## 📋 Features

### Book Management
- Create new books with name, streaming platform, and categories
- View all registered books
- Delete existing books
- Supported streaming platforms:
  - Amazon Kindle (AK)
  - Physical Book (PB)

### Book Evaluation
- Rate books with grades (0-5)
- Add comments to books
- Update existing evaluations

### Smart Recommendations
- Get random book recommendations based on:
  - Minimum grade filter
  - Category filter
  - Read/Unread status

## 🚀 API Endpoints

### GET `/api/books/`
- Returns list of all books
- Response: List of books with name, streaming, categories, and ID

### POST `/api/books/`
- Creates a new book
- Required fields:
  - name: string
  - streaming: string (PB or AK)
  - categories: array of category IDs

### PUT `/api/books/{book_id}`
- Updates book evaluation
- Required fields:
  - comments: string
  - grade: integer (0-5)

### DELETE `/api/books/{book_id}`
- Deletes specified book
- Returns deleted book ID

### GET `/api/books/random/`
- Returns random book based on filters
- Query parameters:
  - min_grade: integer
  - categories: integer
  - read_again: boolean

## 💾 Models

### Books
```python
- name: CharField(max_length=50)
- streaming: CharField(choices=['AK', 'PB'])
- grade: IntegerField(nullable)
- comments: TextField(nullable)
- categories: ManyToManyField(Categories)
```

### Categories
```python
- name: CharField(max_length=50)
```

## 🔧 Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/Caio-Felice-Cunha/API-Book-Reg-Aval.git
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django django-ninja
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start development server:
```bash
python manage.py runserver
```

## ⚖️ Credits

This project was developed as part of the "4 Days 4 Projects" initiative by [Pythonando](https://pythonando.com.br) on YouTube.

## 📝 Note

This is an MVP (Minimum Viable Product) project intended for demonstration and learning purposes. While functional, it may require additional features and security measures for production use.

## 📫 Contact

Caio Felice Cunha - [GitHub Profile](https://github.com/Caio-Felice-Cunha)

Project Link: [https://github.com/Caio-Felice-Cunha/API-Book-Reg-Aval](https://github.com/Caio-Felice-Cunha/API-Book-Reg-Aval)
