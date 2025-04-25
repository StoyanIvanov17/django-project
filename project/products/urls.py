from django.urls import path

from project.products import views

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='products'),
]
