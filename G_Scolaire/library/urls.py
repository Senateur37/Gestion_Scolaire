from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/create/', views.BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    
    path('borrows/', views.BorrowListView.as_view(), name='borrow_list'),
    path('borrows/create/', views.BorrowCreateView.as_view(), name='borrow_create'),
    path('borrows/<int:pk>/update/', views.BorrowUpdateView.as_view(), name='borrow_update'),
]
