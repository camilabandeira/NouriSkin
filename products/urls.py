from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<int:product_id>/write-review/', views.write_review, name='write_review'),
    path('add/', views.add_product, name='add_product'),
    path('product/<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:product_id>/delete/', views.delete_product, name='delete_product'),
]