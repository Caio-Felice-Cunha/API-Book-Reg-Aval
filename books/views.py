from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Books, Categories

class BookListView(ListView):
    model = Books
    template_name = 'books/book_list.html'
    context_object_name = 'books'

def book_create(request):
    if request.method == 'POST':
        grade = request.POST.get('grade')
        book = Books.objects.create(
            name=request.POST.get('name', ''),
            streaming=request.POST.get('streaming', ''),
            grade=int(grade) if grade else None,
            comments=request.POST.get('comments', '')
        )
        book.categories.set(request.POST.getlist('categories'))
        return redirect('book_list')
    
    return render(request, 'books/book_form.html', {
        'categories': Categories.objects.all()
    })
