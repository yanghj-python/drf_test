from django.urls import path

from api import views

urlpatterns = [
    path("books/", views.BookAPIView.as_view()),
    path("books/<str:id>/", views.BookAPIView.as_view()),

    path("tog/books/", views.BookAPIViewTogether.as_view()),
    path("tog/books/<str:id>/", views.BookAPIViewTogether.as_view()),
]