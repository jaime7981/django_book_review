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
