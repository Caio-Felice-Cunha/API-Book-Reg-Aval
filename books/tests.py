import json

from django.test import TestCase

from .models import Books, Categories


class BookAPITests(TestCase):
    """Covers the core API behavior and the bugs fixed during the audit pass.

    Endpoints under test (mounted at /api/books/ via core.api):
      GET    /api/books/
      POST   /api/books/
      GET    /api/books/{id}
      PATCH  /api/books/{id}/rating
      GET    /api/books/random/
    """

    def setUp(self):
        self.fiction = Categories.objects.create(name="Fiction")
        self.science = Categories.objects.create(name="Science")

    def _make_book(self, name, grade=None, comments=None, streaming="PB", cats=None):
        book = Books.objects.create(
            name=name, streaming=streaming, grade=grade, comments=comments
        )
        book.categories.set(cats or [self.fiction.id])
        return book

    # --- list / get -------------------------------------------------------

    def test_list_books_returns_all(self):
        self._make_book("A")
        self._make_book("B")
        resp = self.client.get("/api/books/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 2)

    def test_get_book_by_id(self):
        book = self._make_book("Solo")
        resp = self.client.get(f"/api/books/{book.id}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["name"], "Solo")

    def test_get_missing_book_404(self):
        resp = self.client.get("/api/books/9999")
        self.assertEqual(resp.status_code, 404)

    # --- create -----------------------------------------------------------

    def test_create_book(self):
        payload = {"name": "New", "streaming": "AK", "categories": [self.fiction.id]}
        resp = self.client.post(
            "/api/books/", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Books.objects.filter(name="New").exists())

    # --- view schema exposes grade/comments (was write-only) --------------

    def test_view_schema_exposes_grade_and_comments(self):
        book = self._make_book("Rated", grade=7, comments="nice")
        resp = self.client.get(f"/api/books/{book.id}")
        body = resp.json()
        self.assertEqual(body["grade"], 7)
        self.assertEqual(body["comments"], "nice")

    # --- rating bounds ----------------------------------------------------

    def test_rate_book_within_bounds(self):
        book = self._make_book("Gradeable")
        resp = self.client.patch(
            f"/api/books/{book.id}/rating",
            data=json.dumps({"grade": 8}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        book.refresh_from_db()
        self.assertEqual(book.grade, 8)

    def test_rate_book_rejects_out_of_range(self):
        book = self._make_book("TooHigh")
        resp = self.client.patch(
            f"/api/books/{book.id}/rating",
            data=json.dumps({"grade": 999}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 422)
        book.refresh_from_db()
        self.assertIsNone(book.grade)

    # --- partial patch preserves untouched fields -------------------------

    def test_comments_only_patch_preserves_grade(self):
        book = self._make_book("Keep", grade=7)
        resp = self.client.patch(
            f"/api/books/{book.id}/rating",
            data=json.dumps({"comments": "only comments"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        book.refresh_from_db()
        self.assertEqual(book.grade, 7)
        self.assertEqual(book.comments, "only comments")

    # --- random with filters ----------------------------------------------

    def test_random_with_min_grade_filter(self):
        self._make_book("Low", grade=2)
        self._make_book("High", grade=9)
        resp = self.client.get("/api/books/random/?min_grade=5")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["name"], "High")

    def test_random_with_category_filter(self):
        self._make_book("Sci", grade=8, cats=[self.science.id])
        self._make_book("Fic", grade=8, cats=[self.fiction.id])
        resp = self.client.get(f"/api/books/random/?categories={self.science.id}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["name"], "Sci")

    def test_random_empty_returns_404_not_500(self):
        resp = self.client.get("/api/books/random/")
        self.assertEqual(resp.status_code, 404)
