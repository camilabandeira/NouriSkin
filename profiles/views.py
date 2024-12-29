from django.shortcuts import render
from .models import Profile

def profile(request):
    """ Display the user's profile. """
    return render(request, 'profiles/profile.html')
