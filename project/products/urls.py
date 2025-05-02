from django.urls import path, include

from project.products import views

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='products'),
    path('<int:pk>/<str:gender>/<slug:slug>/', include([
        path('', views.ProductDetailsView.as_view(), name='product-details'),
    ]))
]

