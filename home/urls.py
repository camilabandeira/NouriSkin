from django.urls import path
from .views import homepage, faq_page

urlpatterns = [
    path('', homepage, name='homepage'),
    path('faq/', faq_page, name='faq'),
]