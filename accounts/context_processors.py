from catalog.models import BookInstance, Book


def account_data(request):
    num_loaned_by_user = BookInstance.objects.filter(borrowed=request.user.id).count()
    last_loaned_book = Book.objects.filter(bookinstance__borrowed=request.user.id).order_by('bookinstance__due_back')
    last_title = 'You didnt loan any book'
    if last_loaned_book:
        last_title = last_loaned_book[1].title

    return {'num_loaned_by_user': num_loaned_by_user, 'last_loaned_book_title': last_title}
