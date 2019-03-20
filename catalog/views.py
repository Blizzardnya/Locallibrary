from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from . models import *

# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'catalog/index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_genres': num_genres, 'num_visits': num_visits},
    )


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book/book_list.html'
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book/book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalog/author/author_list.html'
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author/author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/book/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrowed=self.request.user,
            status__exact='o'
        ).order_by('due_back')
