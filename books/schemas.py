from ninja import ModelSchema, Schema
from .models import Books

class BooksSchema(ModelSchema):
    class Meta:
        model = Books
        fields = ['name', 'streaming', 'categories']

class BooksViewSchema(ModelSchema):
    class Meta:
        model = Books
        fields = ['name', 'streaming', 'categories', 'id']

class RatingSchema(ModelSchema):
    class Meta:
        model = Books
        fields = ['grade', 'comments']

class RandomFiltersSchema(Schema):
    min_grade : int = None
    categories : int = None
    read_again: bool = False