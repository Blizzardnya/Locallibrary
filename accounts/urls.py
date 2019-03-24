from django.urls import path, include
from . import views


urlpatterns = [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('loanbooks/', views.LoanedBooksListView.as_view(), name='loan-borrowed'),
]