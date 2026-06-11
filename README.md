# API-Book-Reg-Aval

A small REST API built with Django and django-ninja for registering books, tagging them with categories, and rating them. It also ships a minimal HTML page to list and add books.

This is a learning/portfolio project (see Credits). The code below has been cleaned up so the documented setup actually runs and the rating and random-selection features behave as described.

## What it does

- Register books with a name, a format (Amazon Kindle or Physical Book), and one or more categories.
- Rate a book from 0 to 10 and attach a free-text comment.
- Read a book's rating and comment back through the API.
- Pull a random book, optionally filtered by minimum grade and by category.
- Browse and add books through a Bootstrap HTML page, and manage everything in the Django admin.

## Tech stack

- Python, Django 5.1+ (verified on Django 6.0)
- django-ninja (typed routing + Pydantic schemas)
- django-cors-headers
- SQLite (default Django dev database)

## API endpoints

All endpoints are mounted under `/api/books/`. Interactive docs are at `/api/docs`.

| Method | Path | Purpose | Query / Body |
| ------ | ---- | ------- | ------------ |
| GET | `/api/books/` | List all books | none |
| POST | `/api/books/` | Create a book | body: `name`, `streaming` (`AK` or `PB`), `categories` (list of ids) |
| GET | `/api/books/{id}` | Get one book | none |
| PATCH | `/api/books/{id}/rating` | Update grade and/or comments | body: `grade` (0-10, optional), `comments` (optional) |
| GET | `/api/books/random/` | Get a random book | query: `min_grade` (0-10), `categories` (id) |

Notes on behavior:

- `grade` is validated to the 0-10 range at the request layer; out-of-range values return `422`.
- The rating PATCH is a true partial update. Sending only `comments` leaves an existing `grade` untouched.
- `GET /api/books/random/` returns `404` when no book matches the filters (instead of a 500).
- `grade` and `comments` are included in the response body, so a stored rating is readable through the API.

## Installation and usage

### Prerequisites

- Python 3.10+
- A virtual environment tool (`venv` is fine)

### Setup

1. Clone the repository.
   ```bash
   git clone https://github.com/Caio-Felice-Cunha/API-Book-Reg-Aval.git
   cd API-Book-Reg-Aval
   ```

2. Create and activate a virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Configure environment variables. Copy `.env.example` to `.env` and adjust. The app reads `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` from the environment, with dev-safe defaults if they are unset.

5. Apply migrations.
   ```bash
   python manage.py migrate
   ```

6. (Optional) Load the sample data (10 books across 4 categories) so the API has something to return on first run.
   ```bash
   python manage.py loaddata sample_books
   ```

7. (Optional) Create an admin user for the admin panel.
   ```bash
   python manage.py createsuperuser
   ```

8. Run the server.
   ```bash
   python manage.py runserver
   ```

9. Open the app.
   - HTML book list: http://127.0.0.1:8000/
   - API docs: http://127.0.0.1:8000/api/docs
   - Admin panel: http://127.0.0.1:8000/admin

The database (`db.sqlite3`) is created locally on first migrate and is intentionally git-ignored, so each clone starts clean. Use the fixture in step 6 to seed demo data.

## Running tests

```bash
python manage.py test
```

The suite in `books/tests.py` covers list/get/create, rating bounds rejection, partial-PATCH preservation, random-with-filters, and the empty-random 404.

## Configuration

| Variable | Default | Purpose |
| -------- | ------- | ------- |
| `DJANGO_SECRET_KEY` | dev-only insecure key | Django signing key. Set a real one for any deployment. |
| `DJANGO_DEBUG` | `1` | `1` enables debug mode (local dev). Set `0` for production. |
| `DJANGO_ALLOWED_HOSTS` | empty | Comma-separated hosts. Required when `DJANGO_DEBUG=0`. |

## Project layout

```
core/        Django project (settings, root URLs, ninja API mount)
books/       App: models, schemas, ninja router, HTML views, templates, tests
  fixtures/  sample_books.json seed data
manage.py    Django entrypoint
```

## License

This project is licensed under the [MIT License](LICENSE).

## Credits

Built as part of the "4 Days 4 Projects" initiative by [Pythonando](https://pythonando.com.br) on YouTube.
