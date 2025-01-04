from django.urls import path
from .views import homepage, faq_page, return_refund, about, contact
from django.conf.urls import handler404
from .views import custom_404_view
from .views import search_results



handler404 = custom_404_view

urlpatterns = [
    path('', homepage, name='homepage'),
    path('faq/', faq_page, name='faq'),
    path('return-refund/', return_refund, name='return_refund'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('search/', search_results, name='search_results'),
]