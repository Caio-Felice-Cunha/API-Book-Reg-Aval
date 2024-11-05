from ninja import NinjaAPI
from books.api import books_router

api = NinjaAPI()
api.add_router('books', books_router)
