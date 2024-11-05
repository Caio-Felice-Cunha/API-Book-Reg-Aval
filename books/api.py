from ninja import Router, Query
from .schemas import BooksSchema, RatingSchema, RandomFiltersSchema
from .models import Books, Categories

books_router = Router()


@books_router.post('/')
def create_book(request, book_schema: BooksSchema):
    name = book_schema.dict()['name']
    streaming = book_schema.dict()['streaming']
    categories = book_schema.dict()['categories']

    if streaming not in ['PB', 'AK']:
        return 400, {'status': 'Error: Streaming should be PB or AK'}

    book = Books(
        name=name,
        streaming=streaming
    )

    book.save()

    for category in categories:
        temp_category = Categories.objects.get(id=category)
        book.categories.add(temp_category)



    return {'status': 'ok'}


@books_router.put('/{book_id}')
def rate_book(request, book_id: int, rating_schema: RatingSchema):
    comments = rating_schema.dict()['comments']
    grade = rating_schema.dict()['grade']

    if grade < 0 or grade > 5:
        return 400, {'status': 'Error: the value must be between 1 and 5'}
    try:
        book = Books.objects.get(id=book_id)
        book.comments= comments
        book.grade = grade
        book.save()

        return 200, {'status': 'Your evaluation was successfully done'}
    
    except:
        return 500, {'status': 'Internal server error'}

@books_router.delete('/{book_id}')
def delete_book(request, book_id: int):
    book = Books.objects.get(id=book_id)
    book.delete()
    return book_id


@books_router.get('/random/', response={200:BooksSchema, 404:dict})
def random_book(request, filters: Query[RandomFiltersSchema]):
    min_grade = filters.dict()['min_grade']
    categories = filters.dict()['categories']
    read_again = filters.dict()['read_again']

    books = Books.objects.all()

    if not read_again:
        books = books.filter(grade=None)
    
    if min_grade:
        books = books.filter(grade__gte=min_grade)

    if categories:
        books = books.filter(categories__id = categories)

    book = books.order_by('?').first()

    if books.count() > 0:
        return 200, book
    else:
        return 404, {'status': 'Book not found'}
    


