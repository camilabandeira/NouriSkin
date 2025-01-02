from django.urls import path
from .views import homepage, faq_page, return_refund
from django.conf.urls import handler404
from .views import custom_404_view

handler404 = custom_404_view

urlpatterns = [
    path('', homepage, name='homepage'),
    path('faq/', faq_page, name='faq'),
    path('return-refund/', return_refund, name='return_refund'),
]