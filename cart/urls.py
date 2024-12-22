from django.urls import path
from . import views


urlpatterns = [
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('add/<item_id>/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='view_cart'),
]
