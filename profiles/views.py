from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import ProfileForm
from checkout.models import Order


@login_required
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    orders = Order.objects.filter(profile=profile).order_by('-date')

    paginator = Paginator(orders, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            return redirect('profile')
        else:
            print(form.errors)
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        form = ProfileForm(instance=profile, initial=initial_data)

    return render(request, 'profiles/profile.html', {
        'page_obj': page_obj,
        'form': form,
        'orders': orders,
    })
