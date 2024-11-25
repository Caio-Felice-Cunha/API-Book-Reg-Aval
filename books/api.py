from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from .models import Books
from .schemas import BooksSchema, BooksViewSchema, RatingSchema, RandomFiltersSchema

books_router = Router()

@books_router.get("/", response=List[BooksViewSchema])
def list_books(request):
    """Get all books"""
    return Books.objects.all()

@books_router.post("/", response=BooksViewSchema)
def create_book(request, payload: BooksSchema):
    """Create a new book"""
    book = Books.objects.create(
        name=payload.name,
        streaming=payload.streaming
    )
    book.categories.set(payload.categories)
    return book

@books_router.get("/{book_id}", response=BooksViewSchema)
def get_book(request, book_id: int):
    """Get a specific book by ID"""
    return get_object_or_404(Books, id=book_id)

@books_router.patch("/{book_id}/rating", response=BooksViewSchema)
def rate_book(request, book_id: int, payload: RatingSchema):
    """Update book rating and comments"""
    book = get_object_or_404(Books, id=book_id)
    book.grade = payload.grade
    book.comments = payload.comments
    book.save()
    return book

@books_router.get("/random/", response=BooksViewSchema)
def get_random_book(request, filters: RandomFiltersSchema = None):
    """Get a random book with optional filters"""
    queryset = Books.objects.all()
    
    if filters:
        if filters.min_grade:
            queryset = queryset.filter(grade__gte=filters.min_grade)
        if filters.categories:
            queryset = queryset.filter(categories=filters.categories)
    
    return queryset.order_by('?').first()
    


