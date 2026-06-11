from typing import Optional

from ninja import Field, ModelSchema, Schema

from .models import Books


class BooksSchema(ModelSchema):
    class Meta:
        model = Books
        fields = ['name', 'streaming', 'categories']


class BooksViewSchema(ModelSchema):
    class Meta:
        model = Books
        fields = ['name', 'streaming', 'categories', 'id', 'grade', 'comments', 'created_at']


class RatingSchema(Schema):
    """Partial-update payload for ratings.

    Uses a plain Schema (not ModelSchema) so the 0-10 bound is enforced at
    request validation time, and both fields are optional so a comments-only
    PATCH does not wipe an existing grade.
    """

    grade: Optional[int] = Field(None, ge=0, le=10)
    comments: Optional[str] = None


class RandomFiltersSchema(Schema):
    min_grade: Optional[int] = Field(None, ge=0, le=10)
    categories: Optional[int] = None
