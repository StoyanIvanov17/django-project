from django.urls import path, include

from project.products import views

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='products'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/<slug:slug>/', include([
        path('', views.ProductDetailsView.as_view(), name='product-details'),
    ]))
]

