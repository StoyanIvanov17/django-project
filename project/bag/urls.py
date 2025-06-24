from django.urls import path
from project.bag import views

urlpatterns = [
    path('', views.BagView.as_view(), name='bag'),
    path('api/add/', views.AddToBagView.as_view(), name='api-add-to-bag'),
    path('api/remove/', views.RemoveFromBagView.as_view(), name='api-remove-from-bag'),
    path('api/increase/', views.IncreaseBagItemQuantity.as_view(), name='api-increase-item-quantity'),
]

