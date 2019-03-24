from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),

    path('book/', include([
        path('create/', views.BookCreateView.as_view(), name='book_create'),
        path('<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
        path('<int:pk>/', include([
            path('', views.BookDetailView.as_view(), name='book-detail'),
            path('update/', views.BookUpdateView.as_view(), name='book-update'),
            path('delete/', views.BookDeleteView.as_view(), name='book-delete'),
        ]))
    ])),

    path('author/', include([
        path('create/', views.AuthorCreate.as_view(), name='author_create'),
        path('<int:pk>/', include([
            path('', views.AuthorDetailView.as_view(), name='author-detail'),
            path('update/', views.AuthorUpdate.as_view(), name='author_update'),
            path('delete/', views.AuthorDelete.as_view(), name='author_delete'),
        ]))
    ])),
]
