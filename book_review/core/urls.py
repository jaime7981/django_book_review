from django.urls import path
from . import views as views
from core.scaffolding import BookCrudManager, AuthorCrudManager, CountryCrudManager, ReviewCrudManager, SalesCrudManager
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='main/')),
    path('main/', views.main, name='main'),
    path('authors_info/', views.authorsInfo, name='authors_info'),
    path('books_top_10/', views.booksTop10, name='books_top_10'),
    path('books_top_selling/', views.booksTopSelling, name='books_top_selling'),
    path('search/', views.search, name='search'),
    path('search/<int:pagination_number>/', views.search, name='search'),
    path('authors/create/', views.CreateAuthorView.as_view(), name='create_author'),
    path('authors/update/<int:pk>', views.UpdateAuthorView.as_view(), name='update_author'),
    path('books/create/', views.CreateBookView.as_view(), name='create_book'),
    path('books/update/<int:pk>', views.UpdateBookView.as_view(), name='update_book'),
    path('reviews/create/', views.CreateReviewView.as_view(), name='create_review'),
    path('reviews/update/<int:pk>', views.UpdateReviewView.as_view(), name='update_review'),
    path('sales/create/', views.CreateSaleView.as_view(), name='create_sale'),
    path('sales/update/<int:pk>', views.UpdateSaleView.as_view(), name='update_sale'),
]

book_crud = BookCrudManager()
author_crud = AuthorCrudManager()
country_crud = CountryCrudManager()
review_crud = ReviewCrudManager()
sales_crud = SalesCrudManager()

urlpatterns += book_crud.get_url_patterns()
urlpatterns += author_crud.get_url_patterns()
urlpatterns += country_crud.get_url_patterns()
urlpatterns += review_crud.get_url_patterns()
urlpatterns += sales_crud.get_url_patterns()
