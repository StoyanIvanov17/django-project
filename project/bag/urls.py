from django.urls import path
from project.bag import views

urlpatterns = [
    path('', views.BagView.as_view(), name='bag'),
    path('add/', views.AddToBagView.as_view(), name='add-to-bag'),
]

