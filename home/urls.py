from django.urls import path
from .views import homepage, faq_page, return_refund

urlpatterns = [
    path('', homepage, name='homepage'),
    path('faq/', faq_page, name='faq'),
    path('return-refund/', return_refund, name='return_refund'),
]