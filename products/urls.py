from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.all_products, name='products'),
    path(
        '<int:product_id>/',
        views.product_detail,
        name='product_detail',
    ),
    path(
        '<int:product_id>/write-review/',
        views.write_review,
        name='write_review',
    ),
    path(
        'add/',
        views.add_product,
        name='add_product',
    ),
    path(
        'product/<int:pk>/update/',
        views.product_update,
        name='product_update',
    ),
    path(
        '<int:product_id>/delete/',
        views.delete_product,
        name='delete_product',
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
