from django.urls import path

from project.products import views

urlpatterns = [
    path('view-all/', views.ProductsListView.as_view(), name='all-products'),
    path('<int:pk>/<str:gender>/<slug:slug>/', views.ProductDetailsView.as_view(), name='product-details'),
]
