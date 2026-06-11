from typing import List

from django.shortcuts import get_object_or_404
from ninja import Query, Router

from .models import Books
from .schemas import BooksSchema, BooksViewSchema, RandomFiltersSchema, RatingSchema

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


@books_router.get("/random/", response={200: BooksViewSchema, 404: dict})
def get_random_book(request, filters: Query[RandomFiltersSchema] = None):
    """Get a random book with optional filters (min_grade, categories)."""
    queryset = Books.objects.all()

    if filters:
        if filters.min_grade is not None:
            queryset = queryset.filter(grade__gte=filters.min_grade)
        if filters.categories is not None:
            queryset = queryset.filter(categories=filters.categories)

    book = queryset.order_by('?').first()
    if book is None:
        return 404, {"detail": "No book matches the given filters."}
    return book


@books_router.get("/{book_id}", response=BooksViewSchema)
def get_book(request, book_id: int):
    """Get a specific book by ID"""
    return get_object_or_404(Books, id=book_id)


@books_router.patch("/{book_id}/rating", response=BooksViewSchema)
def rate_book(request, book_id: int, payload: RatingSchema):
    """Update book rating and/or comments.

    Only the fields present in the request body are updated, so a
    comments-only PATCH leaves an existing grade untouched.
    """
    book = get_object_or_404(Books, id=book_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(book, attr, value)
    book.save()
    return book
