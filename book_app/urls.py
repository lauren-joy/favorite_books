from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home),
    path('logout',views.logout),
    path('create', views.create),
    path('edit/<int:book_id>', views.edit),
    path('update/<int:book_id>', views.update),
    path('delete/<int:book_id>', views.delete),
    path('<int:book_id>', views.show),
    path('favorite/<int:book_id>', views.favorite),
    path('unfavorite/<int:book_id>', views.unfavorite),
]