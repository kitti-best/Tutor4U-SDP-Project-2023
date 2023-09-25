from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from django.shortcuts import render, redirect

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile') # change direction of redirect to user profile page
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})