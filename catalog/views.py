import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from . models import *
from .forms import *

# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_languages = Language.objects.all().count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'catalog/index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_genres': num_genres, 'num_visits': num_visits, 'num_languages': num_languages},
    )


# ---------------------------------------------------------Books--------------------------------------------
class BookCreateView(PermissionRequiredMixin, generic.CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'ISBN', 'genre', 'language']

    template_name = 'catalog/book/book_form.html'
    permission_required = ('catalog.can_mark_returned',)


class BookUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Book
    fields = '__all__'
    template_name = 'catalog/book/book_form.html'
    permission_required = ('catalog.can_mark_returned',)


class BookDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    template_name = 'catalog/book/book_confirm_delete.html'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book/book_detail.html'


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book/book_list.html'
    paginate_by = 12


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            return HttpResponseRedirect(reverse('loan-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/book/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


# --------------------------------------------------------------Authors------------------------------------------------
class AuthorCreate(PermissionRequiredMixin, generic.CreateView):
    model = Author
    fields = '__all__'
    template_name = 'catalog/author/author_form.html'
    permission_required = ('catalog.can_mark_returned',)


class AuthorUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'catalog/author/author_form.html'
    permission_required = ('catalog.can_mark_returned',)


class AuthorDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'catalog/author/author_confirm_delete.html'
    permission_required = ('catalog.can_mark_returned',)


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author/author_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalog/author/author_list.html'
    paginate_by = 12


