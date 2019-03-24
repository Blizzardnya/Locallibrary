from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from catalog.models import BookInstance
# Create your views here.


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'accounts/books/bookinstance_list_borrowed_user.html'
    paginate_by = 12

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrowed=self.request.user,
            status__exact='o'
        ).order_by('due_back')[:48]


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'accounts/books/bookinstance_list_borrowed.html'
    paginate_by = 12
    permission_required = ('catalog.can_mark_returned',)

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')[:48]
